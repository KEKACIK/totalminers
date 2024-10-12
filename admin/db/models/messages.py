import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class MessageSender:
    USER = 'user'
    ADMIN = 'admin'


class Message(Model):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id', ondelete='SET NULL'))
    ticket = relationship('Ticket', foreign_keys=ticket_id, uselist=False, lazy='selectin')
    sender = Column(String(length=32))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
