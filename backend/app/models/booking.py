from typing import Optional
from pydantic import BaseModel, Field


class ReturnFlight(BaseModel):
    route: str
    date: str
    scheduled_departure: str
    status: str = "Unaffected"


class Booking(BaseModel):
    booking_reference: str
    customer_id: str
    customer_name: str
    flight_number: str
    route: str
    date: str
    scheduled_departure: str
    original_departure: str
    current_departure: Optional[str] = None
    status: str = Field(..., description="Cancelled, Delayed, or On-time")
    disruption_reason: Optional[str] = None
    delay_hours: float = 0.0
    return_flight: Optional[ReturnFlight] = None
