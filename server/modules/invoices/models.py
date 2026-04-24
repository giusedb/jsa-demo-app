from datetime import date
from typing import List

from pygments.lexer import default
from sqlalchemy import ForeignKey, Float, Date, event
from sqlalchemy.orm import Mapped, relationship, Session
from sqlalchemy.testing.schema import mapped_column

from modules.base import BaseModel

class Provider(BaseModel):
    __tablename__ = 'providers'

    name: Mapped[str]
    address: Mapped[str]

    invoices: Mapped[List["Invoice"]] = relationship(back_populates="provider")


class Invoice(BaseModel):
    __tablename__ = 'invoices'

    provider_id: Mapped[int] = mapped_column(ForeignKey('providers.id'))
    total_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    emitted_on: Mapped[date] = mapped_column(Date, nullable=False, default=lambda : date.today())
    paid_on: Mapped[date] = mapped_column(nullable=True)
    number: Mapped[str]

    provider: Mapped[Provider] = relationship(back_populates="invoices")
    lines: Mapped[List["Line"]] = relationship(back_populates="invoice")

    async def get_total(self):
        total = 0
        for line in await self.awaitable_attrs.lines:
            total += line.quantity * line.price
        return total


class Line(BaseModel):
    __tablename__ = 'lines_of_invoice'

    invoice_id: Mapped[int] = mapped_column(ForeignKey('invoices.id'))
    product: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[float]

    invoice: Mapped[Invoice] = relationship(back_populates="lines")
