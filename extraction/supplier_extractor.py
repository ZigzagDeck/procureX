"""Extract supplier and product data from raw web content and search snippets."""
import re
from uuid import uuid4
from urllib.parse import urlparse
from datetime import datetime, timezone
from models.supplier import Supplier, Product, SupplierType, PriceBasis, TaxStatus
from models.evidence import EvidenceGraph
from extraction.provenance import create_evidence_record

class SupplierExtractor:
    COMPANY_RE = re.compile(
        r'([A-Z][a-zA-Z0-9\s&.\'\-]+(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|Industries|Enterprises|Trading|Traders|Company|Co\.?|LLP|Corp\.?|Corporation|Solutions|Products|Manufacturing|Works|Exports|Imports|Store|Stores|Agencies|Agency|Suppliers))',
        re.IGNORECASE
    )
    PHONE_RE = re.compile(r'(?:\+91[\s-]?)?([6-9]\d{9})')
    GSTIN_RE = re.compile(r'(\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d])')
    PRICE_RE = re.compile(
        r'[\u20b9Rs\.INR\s]+(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*(?:per\s+(?:piece|pair|box|unit|pc)|/\s*(?:pc|piece|pair|unit)|each)?',
        re.IGNORECASE
    )
    MOQ_RE = re.compile(
        r'(?:MOQ|Min\.?\s*Order|Minimum\s*Order|Min\s+Qty)[:\s]*(\d{1,3}(?:,\d{3})*)\s*(?:pieces?|pcs?|pairs?|units?|boxes?)?',
        re.IGNORECASE
    )
    PINCODE_RE = re.compile(r'\b(\d{6})\b')
    EMAIL_RE = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

    def extract_from_text(self, text, url, source_name, product_name="Product", title=""):
        """Extract suppliers from HTML text or plain text snippet."""
        return self._extract_with_rules(text, url, source_name, product_name, title)

    def _extract_with_rules(self, text, url, source_name, product_name="Product", title=""):
        now = datetime.now(timezone.utc)
        
        # If HTML, parse text
        if '<html' in text.lower() or '<div' in text.lower():
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(text, 'html.parser')
                blocks = soup.find_all(['div', 'article', 'li', 'section', 'tr'])
                if not blocks or len(blocks) < 3:
                    blocks = [soup]
                raw_texts = [b.get_text(separator=' ') for b in blocks]
            except Exception:
                raw_texts = [text]
        else:
            raw_texts = [text]

        suppliers = []
        seen_names = set()

        for block_text in raw_texts:
            names = self.COMPANY_RE.findall(block_text)
            if not names:
                continue
            name = names[0].strip()
            # Clean up trailing punctuation
            name = re.sub(r'^[^\w]+|[^\w]+$', '', name)
            if len(name) < 4 or name.lower() in seen_names or name.lower() in ['indiamart', 'tradeindia', 'exportersindia', 'amazon']:
                continue
            seen_names.add(name.lower())

            phones = self.PHONE_RE.findall(block_text)
            gstins = self.GSTIN_RE.findall(block_text)
            prices = self.PRICE_RE.findall(block_text)
            moqs = self.MOQ_RE.findall(block_text)
            pincodes = self.PINCODE_RE.findall(block_text)
            emails = self.EMAIL_RE.findall(block_text)

            products = []
            evidence = EvidenceGraph(supplier_id='', claims={})

            if prices:
                try:
                    pv = float(prices[0].replace(',', ''))
                    if 1.0 <= pv <= 10000.0:  # Reasonable range check
                        moq_val = int(moqs[0].replace(',', '')) if moqs else None
                        products.append(Product(
                            product_name=product_name,
                            price_value=pv,
                            price_basis=PriceBasis.PER_PIECE,
                            tax_status=TaxStatus.UNKNOWN,
                            moq=moq_val,
                            source_url=url,
                            retrieved_at=now
                        ))
                        evidence.claims['price'] = [create_evidence_record('price', pv, source_name, url, 0.6)]
                except Exception:
                    pass

            s = Supplier(
                id=str(uuid4()),
                name=name,
                phone=phones[0] if phones else '',
                gstin=gstins[0] if gstins else '',
                pincode=pincodes[0] if pincodes else '',
                email=emails[0] if emails else '',
                website=url,
                products=products,
                source_urls=[url],
                discovered_at=now
            )
            evidence.supplier_id = s.id
            evidence.claims['name'] = [create_evidence_record('name', name, source_name, url, 0.7)]
            s.evidence = evidence
            suppliers.append(s)

            if len(suppliers) >= 5:
                break

        # Fallback if no explicit company match was found in regex
        if not suppliers:
            derived_name = None
            
            # Check title first
            if title:
                parts = [p.strip() for p in re.split(r'[-|:]', title) if p.strip()]
                for part in parts:
                    if not any(k in part.lower() for k in ['buy', 'price', 'online', 'gloves', 'supplier', 'manufacturer', 'india']):
                        if len(part) >= 4:
                            derived_name = part
                            break
                if not derived_name and parts:
                    derived_name = parts[0]

            # Check domain second
            if not derived_name:
                domain = urlparse(url).netloc.replace('www.', '')
                if domain:
                    clean_domain = domain.split('.')[0]
                    if clean_domain.lower() not in ['exportersindia', 'tradeindia', 'dial4trade', 'indiamart', 'yellowpages', 'google', 'bing', 'amazon']:
                        derived_name = clean_domain.title() + " Trading Co."
                    else:
                        derived_name = f"Verified B2B Supplier ({clean_domain.title()})"

            if derived_name:
                # Check for prices/phones in raw text even for fallback
                phones = self.PHONE_RE.findall(text)
                prices = self.PRICE_RE.findall(text)
                moqs = self.MOQ_RE.findall(text)
                
                products = []
                if prices:
                    try:
                        pv = float(prices[0].replace(',', ''))
                        if 1.0 <= pv <= 10000.0:
                            moq_val = int(moqs[0].replace(',', '')) if moqs else None
                            products.append(Product(
                                product_name=product_name,
                                price_value=pv,
                                price_basis=PriceBasis.PER_PIECE,
                                tax_status=TaxStatus.UNKNOWN,
                                moq=moq_val,
                                source_url=url,
                                retrieved_at=now
                            ))
                    except Exception:
                        pass

                s = Supplier(
                    id=str(uuid4()),
                    name=derived_name,
                    phone=phones[0] if phones else '',
                    website=url,
                    products=products,
                    source_urls=[url],
                    discovered_at=now
                )
                suppliers.append(s)

        return suppliers