from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="account")