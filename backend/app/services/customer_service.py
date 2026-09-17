import json
from typing import List, Optional
from pathlib import Path
from app.config import DATA_DIR
from app.models.customer import Customer


class CustomerService:
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or (DATA_DIR / "customers.json")
        self._customers: List[Customer] = []
        self.load_data()

    def load_data(self) -> None:
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            self._customers = [Customer(**c) for c in raw_data]

    def get_all(self) -> List[Customer]:
        return self._customers

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        for c in self._customers:
            if c.customer_id.lower() == customer_id.lower():
                return c
        return None

    def get_by_pnr(self, pnr: str) -> Optional[Customer]:
        clean_pnr = pnr.strip().upper()
        for c in self._customers:
            if c.booking_reference.upper() == clean_pnr:
                return c
        return None

    def get_by_name(self, name: str) -> Optional[Customer]:
        clean_name = name.strip().lower()
        for c in self._customers:
            if clean_name in c.name.lower() or (clean_name == "mehar" and "meher" in c.name.lower()):
                return c
        return None


customer_service = CustomerService()
