import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agent.budget_manager import BudgetManager
from models.budget import ResearchBudget
from models.supplier import Supplier
from models.scoring import SupplierScore

def test_purchase_high_uncertainty():
    budget = ResearchBudget(initial_budget=0.020, remaining_budget=0.020)
    mgr = BudgetManager(budget)
    supplier = Supplier(name='Test Corp')
    score = SupplierScore(supplier_id=supplier.id, total_score=70)
    decision = mgr.should_purchase_price_intel(supplier, score, price_uncertainty=0.5)
    assert decision.should_purchase == True

def test_skip_low_uncertainty():
    budget = ResearchBudget(initial_budget=0.020, remaining_budget=0.020)
    mgr = BudgetManager(budget)
    supplier = Supplier(name='Test Corp')
    score = SupplierScore(supplier_id=supplier.id, total_score=70)
    decision = mgr.should_purchase_price_intel(supplier, score, price_uncertainty=0.1)
    assert decision.should_purchase == False

def test_skip_insufficient_budget():
    budget = ResearchBudget(initial_budget=0.020, remaining_budget=0.001)
    mgr = BudgetManager(budget)
    supplier = Supplier(name='Test Corp')
    score = SupplierScore(supplier_id=supplier.id, total_score=70)
    decision = mgr.should_purchase_price_intel(supplier, score, price_uncertainty=0.5)
    assert decision.should_purchase == False

def test_verification_purchase():
    budget = ResearchBudget(initial_budget=0.020, remaining_budget=0.020)
    mgr = BudgetManager(budget)
    supplier = Supplier(name='Test Corp')
    score = SupplierScore(supplier_id=supplier.id, total_score=60)
    decision = mgr.should_purchase_verification(supplier, score, verification_score=0.3)
    assert decision.should_purchase == True

def test_decisions_tracked():
    budget = ResearchBudget(initial_budget=0.020, remaining_budget=0.020)
    mgr = BudgetManager(budget)
    supplier = Supplier(name='Test Corp')
    score = SupplierScore(supplier_id=supplier.id, total_score=70)
    mgr.should_purchase_price_intel(supplier, score, 0.5)
    mgr.should_purchase_verification(supplier, score, 0.3)
    assert len(budget.decisions) == 2
