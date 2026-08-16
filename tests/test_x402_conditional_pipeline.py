import asyncio

from agent.orchestrator import ResearchOrchestrator
from models.budget import ResearchBudget
from models.requirement import ProcurementRequirement
from models.supplier import PriceBasis, Product, Supplier, SupplierType, TaxStatus
from storage.session import ResearchSession


def _requirement():
    return ProcurementRequirement(
        product_category="safety_gloves", material="nitrile", application="industrial_safety",
        size="M", quantity=5000, maximum_unit_price=80, destination="Ghaziabad",
    )


def test_paid_price_correction_changes_score(monkeypatch):
    """The uncertain box price is corrected only after a paid x402 lookup."""
    orchestrator = ResearchOrchestrator()
    requirement = _requirement()
    session = ResearchSession(requirement=requirement, budget=ResearchBudget())
    trusted = [
        Supplier(name="Trusted A", supplier_type=SupplierType.MANUFACTURER, gstin="A", phone="1", website="https://a.example", products=[Product(product_name="Gloves", material="nitrile", application="industrial_safety", size="M", price_value=60, price_basis=PriceBasis.PER_PIECE, tax_status=TaxStatus.GST_EXCLUSIVE, moq=1000)]),
        Supplier(name="Trusted B", supplier_type=SupplierType.MANUFACTURER, gstin="B", phone="2", website="https://b.example", products=[Product(product_name="Gloves", material="nitrile", application="industrial_safety", size="M", price_value=70, price_basis=PriceBasis.PER_PIECE, tax_status=TaxStatus.GST_EXCLUSIVE, moq=1000)]),
    ]
    risky = Supplier(name="Risky Box Quote", supplier_type=SupplierType.MANUFACTURER, gstin="C", phone="3", website="https://c.example", products=[Product(product_name="Gloves", material="nitrile", application="industrial_safety", size="M", price_value=240, price_basis=PriceBasis.PER_BOX, tax_status=TaxStatus.GST_EXCLUSIVE, moq=1000)])
    risky.products[0].normalized_unit_price = 240
    score_before_correction = orchestrator.scoring_engine.score_supplier(risky, requirement).total_score
    risky.products[0].normalized_unit_price = None
    session.suppliers = trusted + [risky]

    async def no_search(*args, **kwargs): return []
    async def no_evidence(*args, **kwargs): return None
    monkeypatch.setattr(orchestrator.search_source, "search", no_search)
    monkeypatch.setattr(orchestrator.evidence_collector, "collect_evidence", no_evidence)

    asyncio.run(orchestrator.run_research(requirement, session))

    corrected = risky.products[0]
    score = next(item for item in session.scores if item.supplier_id == risky.id)
    assert len(session.budget.transactions) == 1
    assert session.budget.transactions[0].status.value == "completed"
    assert corrected.normalized_unit_price == 65.0
    assert "₹240.00 → ₹65.00" in corrected.price_correction_note
    assert score.total_score > score_before_correction
    assert any("Price intelligence approved" in entry.message for entry in session.log)


def test_no_low_confidence_quote_means_no_payment(monkeypatch):
    orchestrator = ResearchOrchestrator()
    requirement = _requirement()
    session = ResearchSession(requirement=requirement, budget=ResearchBudget())
    session.suppliers = [
        Supplier(name=f"Trusted {index}", supplier_type=SupplierType.MANUFACTURER, gstin=f"A{index}", phone=str(index), website=f"https://{index}.example", products=[Product(product_name="Gloves", material="nitrile", application="industrial_safety", size="M", price_value=60 + index, price_basis=PriceBasis.PER_PIECE, tax_status=TaxStatus.GST_EXCLUSIVE, moq=1000)])
        for index in range(3)
    ]

    async def no_search(*args, **kwargs): return []
    async def no_evidence(*args, **kwargs): return None
    monkeypatch.setattr(orchestrator.search_source, "search", no_search)
    monkeypatch.setattr(orchestrator.evidence_collector, "collect_evidence", no_evidence)
    asyncio.run(orchestrator.run_research(requirement, session))

    assert session.budget.transactions == []
