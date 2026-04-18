"""Invoice model - Data class for Invoice entity."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class Invoice:
    """Represents an invoice in the hospital system."""

    invoice_id: str
    patient_id: str
    invoice_date: date
    total_amount: Decimal = field(default=Decimal('0.00'))

    def __post_init__(self):
        """
        Validate data after initialization.

        TODO: Convert total_amount to Decimal if it's int/float
        TODO: Raise ValueError if total_amount < 0
        HINT: if isinstance(self.total_amount, (int, float)):
                  self.total_amount = Decimal(str(self.total_amount))
        """
        if isinstance(self.total_amount, (int, float)):
            self.total_amount = Decimal(str(self.total_amount))
        if self.total_amount < 0:
            raise ValueError(f"Total amount cannot be negative: {self.total_amount}")

    def to_dict(self) -> dict:
        """
        Convert Invoice to dictionary.

        TODO: Return dict with keys: InvoiceID, PatientID, InvoiceDate, TotalAmount
        """
        return {
            'InvoiceID': self.invoice_id,
            'PatientID': self.patient_id,
            'InvoiceDate': self.invoice_date.isoformat(),
            'TotalAmount': float(self.total_amount)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Invoice':
        """
        Create Invoice from database row dict.

        TODO: Handle date and Decimal conversion
        """
        inv_date = data['InvoiceDate']
        if isinstance(inv_date, str):
            inv_date = date.fromisoformat(inv_date)
        return cls(
            invoice_id=data['InvoiceID'],
            patient_id=data['PatientID'],
            invoice_date=inv_date,
            total_amount=Decimal(str(data.get('TotalAmount', 0)))
        )

    def __str__(self):
        return f"[{self.invoice_id}] Patient:{self.patient_id} Amount:{self.total_amount}"
