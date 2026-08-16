import os
from models.budget import ResearchBudget, PaymentDecision, ServiceType
from models.scoring import SupplierScore

class BudgetManager:
    def __init__(self, budget: ResearchBudget):
        self.budget = budget
        self.price_intel_cost = float(os.environ.get('PROCUREX_PRICE_INTEL_COST', '0.002'))
        self.supplier_verify_cost = float(os.environ.get('PROCUREX_SUPPLIER_VERIFY_COST', '0.001'))
    
    def should_purchase_price_intel(
        self,
        supplier,
        score: SupplierScore,
        price_uncertainty: float,
        reference_data_available: bool = True,
    ) -> PaymentDecision:
        cost = self.price_intel_cost
        should = (
            price_uncertainty > 0.2 and  # High uncertainty
            score.total_score >= 50 and   # Finalist
            reference_data_available and  # Do not pay when no correction is possible
            self.budget.can_afford(cost)
        )
        if not reference_data_available:
            reason = "Skipped: no high-confidence market reference price is available for this category"
        else:
            reason = f"Price uncertainty: {price_uncertainty:.0%}, Score: {score.total_score:.0f}, Budget: ${self.budget.remaining_budget:.3f}"
        decision = PaymentDecision(
            service_type=ServiceType.PRICE_INTELLIGENCE,
            supplier_id=supplier.id, supplier_name=supplier.name,
            should_purchase=should, cost=cost,
            reason=reason,
            expected_value="Market price validation for cost comparison" if should else "",
        )
        self.budget.decisions.append(decision)
        return decision
    
    def should_purchase_verification(self, supplier, score: SupplierScore, verification_score: float) -> PaymentDecision:
        cost = self.supplier_verify_cost
        should = (
            verification_score < 0.5 and  # Low verification
            score.total_score >= 50 and
            self.budget.can_afford(cost)
        )
        decision = PaymentDecision(
            service_type=ServiceType.SUPPLIER_VERIFICATION,
            supplier_id=supplier.id, supplier_name=supplier.name,
            should_purchase=should, cost=cost,
            reason=f"Verification score: {verification_score:.0%}, Score: {score.total_score:.0f}, Budget: ${self.budget.remaining_budget:.3f}",
            expected_value="Enhanced business verification" if should else "",
        )
        self.budget.decisions.append(decision)
        return decision
