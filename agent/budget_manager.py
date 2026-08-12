import os
from models.budget import ResearchBudget, PaymentDecision, ServiceType
from models.scoring import SupplierScore

class BudgetManager:
    def __init__(self, budget: ResearchBudget):
        self.budget = budget
        self.price_intel_cost = float(os.environ.get('PROCUREX_PRICE_INTEL_COST', '0.002'))
    
    def should_purchase_price_intel(self, supplier, score: SupplierScore, price_uncertainty: float) -> PaymentDecision:
        cost = self.price_intel_cost
        should = (
            price_uncertainty > 0.2 and  # High uncertainty
            score.total_score >= 40 and   # Candidate threshold
            self.budget.can_afford(cost)
        )
        decision = PaymentDecision(
            service_type=ServiceType.PRICE_INTELLIGENCE,
            supplier_id=supplier.id, supplier_name=supplier.name,
            should_purchase=should, cost=cost,
            reason=f"Price uncertainty: {price_uncertainty:.0%}, Score: {score.total_score:.0f}, Budget: ${self.budget.remaining_budget:.3f}",
            expected_value="Market price validation for cost comparison" if should else "",
        )
        self.budget.decisions.append(decision)
        return decision

    def should_purchase_verification(self, supplier, score: SupplierScore, verification_score: float) -> PaymentDecision:
        """Extensible stub: Supplier verification micro-payments deactivated for presentation build."""
        decision = PaymentDecision(
            service_type=ServiceType.SUPPLIER_VERIFICATION,
            supplier_id=supplier.id, supplier_name=supplier.name,
            should_purchase=False, cost=0.0,
            reason="Supplier verification service paused for presentation build",
            expected_value="",
        )
        return decision
