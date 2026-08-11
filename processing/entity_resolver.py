"""Entity resolution / deduplication for suppliers."""
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse
from models.supplier import Supplier

class EntityResolver:
    SUFFIXES = re.compile(r'\b(pvt\.?|ltd\.?|private|limited|inc\.?|corp\.?|llp|industries|enterprises|trading|company|co\.?|solutions|products|manufacturing)\b', re.IGNORECASE)
    def find_duplicates(self, suppliers):
        dupes = []
        for i in range(len(suppliers)):
            for j in range(i+1, len(suppliers)):
                s1, s2 = suppliers[i], suppliers[j]
                if s1.is_duplicate_of or s2.is_duplicate_of: continue
                if self._is_duplicate(s1, s2): dupes.append((s1.id, s2.id))
        return dupes
    def _is_duplicate(self, s1, s2):
        if s1.gstin and s2.gstin and s1.gstin == s2.gstin: return True
        if s1.phone and s2.phone and self._norm_phone(s1.phone) == self._norm_phone(s2.phone): return True
        if s1.email and s2.email and s1.email.lower().strip() == s2.email.lower().strip(): return True
        sim = self._name_sim(s1.name, s2.name)
        if sim >= 0.85:
            if s1.city and s2.city and s1.city.lower() != s2.city.lower(): return False
            return True
        return False
    def merge_suppliers(self, primary, duplicate):
        primary.source_urls = list(set(primary.source_urls + duplicate.source_urls))
        primary.products.extend(duplicate.products)
        for f in ['phone','email','gstin','website','address','city']:
            if not getattr(primary, f) and getattr(duplicate, f): setattr(primary, f, getattr(duplicate, f))
        primary.certifications = list(set(primary.certifications + duplicate.certifications))
        primary.claims = list(set(primary.claims + duplicate.claims))
        duplicate.is_duplicate_of = primary.id
        return primary
    def _norm_name(self, name):
        n = self.SUFFIXES.sub('', name.lower().strip())
        return re.sub(r'[^a-z0-9\s]', '', re.sub(r'\s+', ' ', n)).strip()
    def _norm_phone(self, phone):
        d = re.sub(r'[^0-9]', '', phone)
        return d[-10:] if len(d) >= 10 else d
    def _name_sim(self, n1, n2):
        a, b = self._norm_name(n1), self._norm_name(n2)
        return SequenceMatcher(None, a, b).ratio() if a and b else 0.0
