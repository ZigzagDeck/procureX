import pytest
from datetime import datetime

# Assuming these models will be available in the project structure
from models.requirement import ProcurementRequirement
from models.supplier import Supplier
from models.evidence import EvidenceRecord
from models.budget import ResearchBudget
from storage.session import ResearchSession

@pytest.fixture
def sample_requirement():
    return ProcurementRequirement(
        query="Medical-grade nitrile examination gloves (powder-free, ASTM D6319 compliant), 100,000 boxes/month",
        location="India",
        delivery_location="Mumbai, Maharashtra, India"
    )

@pytest.fixture
def sample_supplier():
    return Supplier(
        id="sup_123",
        name="Global Medical Supplies Ltd.",
        location="Pune, Maharashtra",
        products=[{"name": "Nitrile Examination Gloves", "specifications": "Powder-free, ASTM D6319"}],
        contact_info={"email": "sales@globalmed.example.com", "phone": "+91 9876543210"}
    )

@pytest.fixture
def sample_evidence():
    return EvidenceRecord(
        supplier_id="sup_123",
        claim="Manufacturer of ASTM D6319 gloves",
        source_url="https://globalmed.example.com/certifications",
        snippet="Our Pune facility produces powder-free nitrile gloves strictly adhering to ASTM D6319 standards.",
        confidence_score=0.9
    )

@pytest.fixture
def sample_budget():
    return ResearchBudget(
        initial_balance=0.020,
        current_balance=0.015,
        currency="ETH"
    )

@pytest.fixture
def sample_session(sample_requirement, sample_supplier, sample_budget):
    session = ResearchSession(
        requirement=sample_requirement,
        budget=sample_budget
    )
    session.suppliers.append(sample_supplier)
    return session
