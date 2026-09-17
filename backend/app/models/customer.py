from typing import Optional
from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    email: str
    phone: str


class TravelHistory(BaseModel):
    flights_last_12_months: int
    prior_complaints_count: int
    previous_complaint_details: Optional[str] = None
    previous_resolution: Optional[str] = None


class Customer(BaseModel):
    customer_id: str
    name: str
    loyalty_tier: str = Field(..., description="Gold, Silver, Platinum, or Standard")
    booking_reference: str
    contact: ContactInfo
    travel_history: TravelHistory
