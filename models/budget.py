from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import uuid4

class PaymentStatus(str, Enum):
    """Status of a payment transaction."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class ServiceType(str, Enum):
    """Type of paid external service."""
    PRICE_INTELLIGENCE = "price_intelligence"
    SUPPLIER_VERIFICATION = "supplier_verification"

class PaymentDecision(BaseModel):
    """A decision made on whether to purchase external API data."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    service_type: ServiceType
    supplier_id: str
    supplier_name: str = ""
    should_purchase: bool
    reason: str
    expected_value: str = ""  # Why it's valuable
    cost: float
    decided_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentTransaction(BaseModel):
    """A payment transaction for a service."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    service_type: ServiceType
    supplier_id: str
    amount: float
    currency: str = "USD"
    amount_inr: float = 0.0
    fx_rate: float = 0.0
    status: PaymentStatus = PaymentStatus.PENDING
    decision: PaymentDecision
    response_summary: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: str = ""

class ResearchBudget(BaseModel):
    """Tracks research budget for agent operations."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    initial_budget: float = 0.020  # USD
    remaining_budget: float = 0.020
    total_spent: float = 0.0
    prepaid_balance_usd: float = 0.0
    transactions: list[PaymentTransaction] = Field(default_factory=list)
    decisions: list[PaymentDecision] = Field(default_factory=list)  # all decisions, including skips
    
    def can_afford(self, cost: float) -> bool:
        """Check if remaining budget is enough for cost."""
        return self.remaining_budget >= cost
    
    def record_purchase(self, transaction: PaymentTransaction) -> None:
        """Record a purchase and update budget balances."""
        self.transactions.append(transaction)
        if transaction.status == PaymentStatus.COMPLETED:
            self.total_spent += transaction.amount
            self.remaining_budget -= transaction.amount
