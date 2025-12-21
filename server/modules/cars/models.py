from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from modules.base import BaseModel

class Manifacturer(BaseModel):
    __tablename__ = 'manifacturers'
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    cars: Mapped[list['Car']] = relationship(back_populates='manifacturer')

class Car(BaseModel):
    __tablename__ = 'cars'
    model: Mapped[str] = mapped_column(unique=True)
    plate: Mapped[str] = mapped_column(unique=True, nullable=False)
    manifacturer_id: Mapped[int] = mapped_column(ForeignKey('manifacturers.id'), nullable=False)
    manifacturer: Mapped['Manifacturer'] = relationship(back_populates='cars')

