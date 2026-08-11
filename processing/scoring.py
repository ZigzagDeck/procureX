"""Deterministic supplier scoring engine."""
from models.scoring import SupplierScore, ScoreDimension, ScoringWeights
from models.requirement import ProcurementMode
from processing.price_normalizer import PriceNormalizer
from processing.product_matcher import ProductMatcher
from processing.moq_validator import MOQValidator
from datetime import datetime

class ScoringEngine:
    def __init__(self):
        self.price_normalizer = PriceNormalizer()
        self.product_matcher = ProductMatcher()
        self.moq_validator = MOQValidator()
    def score_supplier(self, supplier, requirement, delivery=None, evidence_graph=None):
        weights = ScoringWeights.for_mode(requirement.procurement_mode)
        dims = []
        pf = self._score_product_fit(supplier, requirement)
        dims.append(ScoreDimension(name='Product Fit', weight=weights.product_fit, raw_score=pf, weighted_score=pf*weights.product_fit))
        pr = self._score_price(supplier, requirement)
        dims.append(ScoreDimension(name='Price Competitiveness', weight=weights.price_competitiveness, raw_score=pr, weighted_score=pr*weights.price_competitiveness))
        vr = self._score_verification(supplier, evidence_graph)
        dims.append(ScoreDimension(name='Business Verification', weight=weights.business_verification, raw_score=vr, weighted_score=vr*weights.business_verification))
        dl = self._score_delivery(delivery)
        dims.append(ScoreDimension(name='Delivery Feasibility', weight=weights.delivery_feasibility, raw_score=dl, weighted_score=dl*weights.delivery_feasibility))
        mq = self._score_moq(supplier, requirement)
        dims.append(ScoreDimension(name='MOQ Compatibility', weight=weights.moq_compatibility, raw_score=mq, weighted_score=mq*weights.moq_compatibility))
        eq = self._score_evidence_quality(evidence_graph)
        dims.append(ScoreDimension(name='Evidence Quality', weight=weights.evidence_quality, raw_score=eq, weighted_score=eq*weights.evidence_quality))
        total = sum(d.weighted_score for d in dims)
        conf = self._calculate_confidence(evidence_graph)
        return SupplierScore(supplier_id=supplier.id, total_score=total, dimensions=dims, confidence=conf, procurement_mode=requirement.procurement_mode, scored_at=datetime.utcnow())
    def _score_product_fit(self, supplier, req):
        if not supplier.products: return 0.3
        best = 0.0
        for p in supplier.products:
            result = self.product_matcher.match_product(req, p)
            score = sum([0.4 if result['material_match'] else 0, 0.3 if result['application_match'] else 0, 0.3 if result['size_match'] else 0])
            best = max(best, score)
        return best
    def _score_price(self, supplier, req):
        if not req.maximum_unit_price: return 0.5
        prices = [p.normalized_unit_price or p.price_value for p in supplier.products if p.price_value]
        if not prices: return 0.3
        return self.price_normalizer.price_competitiveness_score(min(prices), req.maximum_unit_price)
    def _score_verification(self, supplier, evidence_graph):
        score = 0.2
        if supplier.gstin: score += 0.3
        if supplier.phone: score += 0.1
        if supplier.email: score += 0.1
        if supplier.website: score += 0.1
        if evidence_graph and 'gstin' in evidence_graph.claims: score += 0.2
        return min(score, 1.0)
    def _score_delivery(self, delivery):
        if not delivery: return 0.5
        if delivery.is_feasible is True: return 1.0
        elif delivery.is_feasible is False: return 0.2
        return 0.5
    def _score_moq(self, supplier, req):
        moqs = [p.moq for p in supplier.products if p.moq is not None]
        if not moqs: return 0.5
        return self.moq_validator.validate(min(moqs), req.quantity)['score']
    def _score_evidence_quality(self, eg):
        if not eg: return 0.2
        total_records = sum(len(rs) for rs in eg.claims.values())
        if total_records == 0: return 0.2
        if eg.contradictions: return 0.3
        if total_records >= 5: return 0.9
        elif total_records >= 3: return 0.7
        return 0.5
    def _calculate_confidence(self, eg):
        if not eg: return 0.2
        from verification.evidence_graph import EvidenceGraphManager
        return EvidenceGraphManager().calculate_confidence(eg)
