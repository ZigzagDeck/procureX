from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Coordinates(BaseModel):
    """Geographic coordinates."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    latitude: float
    longitude: float
    source: str = ""  # geocoding provider
    confidence: float = 0.0

class RouteEstimate(BaseModel):
    """An estimated route between two coordinates."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    origin: Coordinates
    destination: Coordinates
    distance_km: float
    estimated_duration_hours: float
    route_source: str = ""  # routing provider
    is_estimate: bool = True  # always True; never claim guarantee

class DeliveryFeasibility(BaseModel):
    """Analysis of delivery feasibility based on geographic data."""
    model_config = ConfigDict(from_attributes=True, frozen=False)
    
    supplier_id: str
    supplier_location: Optional[Coordinates] = None
    destination: Optional[Coordinates] = None
    route: Optional[RouteEstimate] = None
    deadline_days: Optional[int] = None
    is_feasible: Optional[bool] = None  # None = unknown
    feasibility_explanation: str = ""
    # IMPORTANT: This is a ROUTE ESTIMATE, not a supplier delivery promise
    disclaimer: str = "Route estimate only. Does not represent supplier delivery commitment."
