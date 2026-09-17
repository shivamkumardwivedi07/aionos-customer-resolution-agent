import json
from typing import List, Optional
from pathlib import Path
from app.config import DATA_DIR
from app.models.booking import Booking


class BookingService:
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or (DATA_DIR / "bookings.json")
        self._bookings: List[Booking] = []
        self.load_data()

    def load_data(self) -> None:
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            self._bookings = [Booking(**b) for b in raw_data]

    def get_all(self) -> List[Booking]:
        return self._bookings

    def get_by_pnr(self, pnr: str) -> Optional[Booking]:
        clean_pnr = pnr.strip().upper()
        for b in self._bookings:
            if b.booking_reference.upper() == clean_pnr:
                return b
        return None

    def get_by_customer_id(self, customer_id: str) -> List[Booking]:
        clean_id = customer_id.strip().lower()
        return [b for b in self._bookings if b.customer_id.lower() == clean_id]

    def get_by_flight_number(self, flight_no: str) -> Optional[Booking]:
        clean_no = flight_no.strip().replace(" ", "").upper()
        for b in self._bookings:
            if b.flight_number.replace(" ", "").upper() == clean_no:
                return b
        return None


booking_service = BookingService()
