from datetime import date
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
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
    total_amount: Mapped[float]
    emitted_on: Mapped[date]
    paid_on: Mapped[date] = mapped_column(nullable=True)

    provider: Mapped[Provider] = relationship(back_populates="invoices")
    lines: Mapped[List["Line"]] = relationship(back_populates="invoice")


class Line(BaseModel):
    __tablename__ = 'lines_of_invoice'

    invoice_id: Mapped[int] = mapped_column(ForeignKey('invoices.id'))
    product: Mapped[str]
    amount: Mapped[float]

    invoice: Mapped[Invoice] = relationship(back_populates="lines")


