from sqlalchemy import create_engine, Column, DateTime, func, Integer, ForeignKey
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, Mapped, relationship, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from .dblog import DbLogMixin

def get_engine(config: dict) -> [Engine, Session]:
    connection = config['connection']
    engine = create_async_engine(connection['string'], )
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    return engine, Session

def get_sync_engine(config: dict) -> Engine:
    connection = config['connection']
    engine = create_engine(connection['string'])
    Session = sessionmaker(bind=engine)
    return engine, Session


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Base model for all models."""

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}[{self.id}]>'

    __str__ = __repr__

