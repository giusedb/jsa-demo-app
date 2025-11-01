from datetime import datetime

from sqlalchemy import Column, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, relationship

from jsalchemy_web_context import session


def get_current_user_id() -> int | None:
    """find the user associated with current session"""
    user = session.user
    if user:
        return user['id']
    return None

def get_now():
    return datetime.now()


class DbLogMixin:

    __expose_fields__ = {
        'created_at': {'readonly': True, 'hidden': True},
        'created_by_id': {'readonly': True, 'hidden': True},
        'last_updated_at': {'readonly': True, 'hidden': True},
        'last_updated_by_id': {'readonly': True, 'hidden': True},
    }

    created_at: Mapped[datetime] = Column(DateTime, default=get_now)
    created_by_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), default=get_current_user_id)
    last_updated_at: Mapped[datetime] = Column(DateTime, onupdate=get_now)
    last_updated_by_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), onupdate=get_current_user_id)

    @declared_attr
    def creator(self) -> Mapped["User"]:
        return relationship('User', foreign_keys=[self.created_by_id])

    @declared_attr
    def updated_by(self):
        return relationship('User', foreign_keys=[self.last_updated_by_id])