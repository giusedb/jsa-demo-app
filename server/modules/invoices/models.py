from datetime import date
from typing import List

from sqlalchemy import ForeignKey, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from modules.base import BaseModel


class Provider(BaseModel):
    __tablename__ = 'providers'

    name: Mapped[str]
    address: Mapped[str]

    invoices: Mapped[List["Invoice"]] = relationship(
        back_populates="provider",
    )


class Invoice(BaseModel):
    __tablename__ = 'invoices'

    provider_id: Mapped[int] = mapped_column(ForeignKey('providers.id', ondelete='CASCADE'))
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    emitted_on: Mapped[date] = mapped_column(Date, nullable=False, default=lambda: date.today())
    paid_on: Mapped[date] = mapped_column(nullable=True)
    number: Mapped[str]

    provider: Mapped[Provider] = relationship(back_populates="invoices")
    lines: Mapped[List["Line"]] = relationship(back_populates="invoice")

    def get_lines_total(self) -> float:
        """Compute total from lines synchronously (no DB round-trip)."""
        return sum(line.quantity * line.price for line in self.lines)


class Line(BaseModel):
    __tablename__ = 'lines_of_invoice'

    invoice_id: Mapped[int] = mapped_column(ForeignKey('invoices.id', ondelete='CASCADE'))
    product: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[float]

    invoice: Mapped[Invoice] = relationship(back_populates="lines")

    @validates('price', 'quantity')
    def validate_positive(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key} must be non-negative, got {value}')
        return value