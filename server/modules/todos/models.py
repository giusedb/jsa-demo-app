from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from modules.base import BaseModel

class Todo(BaseModel):
    __tablename__ = 'todos'
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool]= mapped_column(Boolean, default=False)
