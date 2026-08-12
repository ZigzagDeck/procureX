"""Extract supplier and product data from raw web content."""
import re, os
from datetime import datetime
from uuid import uuid4
from urllib.parse import urlparse
from models.supplier import Supplier, Product, SupplierType, PriceBasis, TaxStatus
from models.evidence import EvidenceGraph
from extraction.provenance import create_evidence_record

class SupplierExtractor:
    COMPANY_RE = re.compile(r'([A-Z][a-zA-Z\s&.]+(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|Industries|Enterprises|Trading|Company|LLP|Corp\.?|Solutions|Products|Manufacturing))', re.IGNORECASE)
    PHONE_RE = re.compile(r'(?:\+91[\s-]?)?([6-9]\d{9})')
    GSTIN_RE = re.compile(r'(\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d])')
    PRICE_RE = re.compile(r'[\u20b9Rs\.INR\s]+(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*(?:per\s+(?:piece|pair|box|unit)|/\s*(?:pc|piece|pair|unit))', re.IGNORECASE)
    MOQ_RE = re.compile(r'(?:MOQ|Min\.?\s*Order|Minimum\s*Order)[:\s]*(\d{1,3}(?:,\d{3})*)\s*(?:pieces?|pcs?|pairs?|units?)?', re.IGNORECASE)
    PINCODE_RE = re.compile(r'\b(\d{6})\b')
    EMAIL_RE = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

    def extract_from_text(self, text, url, source_name, product_name="Product"):
        return self._extract_with_rules(text, url, source_name, product_name)

    def _extract_with_rules(self, text, url, source_name, product_name="Product"):
        from bs4 import BeautifulSoup
        now = datetime.utcnow()
        soup = BeautifulSoup(text, 'html.parser')
        
        # Divide document into structural container blocks to isolate company data
        blocks = soup.find_all(['div', 'article', 'li', 'section', 'tr'])
        if not blocks or len(blocks) < 3:
            blocks = [soup]
            
        suppliers = []
        seen_names = set()
        
        for block in blocks:
            block_text = block.get_text(separator=' ')
            names = self.COMPANY_RE.findall(block_text)
            if not names:
                continue
            name = names[0].strip()
            if len(name) < 3 or name.lower() in seen_names:
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
                pv = float(prices[0].replace(',', ''))
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
                
            s = Supplier(
                id=str(uuid4()),
                name=name,
                phone=phones[0] if phones else '',
                gstin=gstins[0] if gstins else '',
                pincode=pincodes[0] if pincodes else '',
                email=emails[0] if emails else '',
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
                
        # Fallback if block splitting yielded no results
        if not suppliers:
            domain = urlparse(url).netloc.replace('www.', '')
            if domain:
                name = domain.split('.')[0].title()
                s = Supplier(id=str(uuid4()), name=name, source_urls=[url], discovered_at=now)
                suppliers.append(s)
                
        return suppliers