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

    def extract_from_text(self, text, url, source_name):
        return self._extract_with_rules(text, url, source_name)

    def _extract_with_rules(self, text, url, source_name):
        now = datetime.utcnow()
        names = list(set(self.COMPANY_RE.findall(text)))
        phones = list(set(self.PHONE_RE.findall(text)))
        gstins = list(set(self.GSTIN_RE.findall(text)))
        prices = self.PRICE_RE.findall(text)
        moqs = self.MOQ_RE.findall(text)
        pincodes = list(set(self.PINCODE_RE.findall(text)))
        emails = list(set(self.EMAIL_RE.findall(text)))
        if not names:
            domain = urlparse(url).netloc.replace('www.', '')
            if domain: names = [domain.split('.')[0].title()]
        suppliers = []
        for i, name in enumerate(names[:5]):
            name = name.strip()
            if len(name) < 3: continue
            evidence = EvidenceGraph(supplier_id='', claims={})
            products = []
            if prices:
                pv = float(prices[0].replace(',', ''))
                products.append(Product(product_name='Safety Gloves', price_value=pv, price_basis=PriceBasis.PER_PIECE, tax_status=TaxStatus.UNKNOWN, moq=int(moqs[0].replace(',','')) if moqs else None, source_url=url, retrieved_at=now))
                evidence.claims['price'] = [create_evidence_record('price', pv, source_name, url, 0.5)]
            s = Supplier(id=str(uuid4()), name=name, phone=phones[i] if i<len(phones) else '', gstin=gstins[i] if i<len(gstins) else '', pincode=pincodes[0] if pincodes else '', email=emails[i] if i<len(emails) else '', products=products, source_urls=[url], discovered_at=now)
            evidence.supplier_id = s.id
            evidence.claims['name'] = [create_evidence_record('name', name, source_name, url, 0.6)]
            s.evidence = evidence
            suppliers.append(s)
        return suppliers
