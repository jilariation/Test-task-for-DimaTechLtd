from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)

    account = relationship("Account", back_populates="payments")