import datetime

from sqlalchemy import Column, String, Integer, Boolean, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..base_model import Model


class MinerItem(Model):
    """
    Модель для товаров (майнеры которые покупают)
    """
    __tablename__ = 'miner_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    hash_rate = Column(BigInteger, default=0)
    energy_consumption = Column(Integer, default=0)
    price = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('miner_items_categories.id', ondelete='SET NULL'))
    category = relationship('MinerItemCategory', foreign_keys=category_id, uselist=False, lazy='selectin')
    image_id = Column(Integer, ForeignKey('images.id', ondelete='SET NULL'), nullable=True)
    image = relationship('Image', foreign_keys=image_id, uselist=False, lazy='selectin')
    income = Column(Integer, default=0)
    hosting = Column(Integer, default=0)
    profit = Column(Integer, default=0)
    is_hidden = Column(Boolean, default=False)
    priority = Column(Integer, default=0)
    discount_count = Column(Integer, default=0)
    discount_value = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.datetime.now)
