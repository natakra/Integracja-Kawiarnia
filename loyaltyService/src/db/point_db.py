from sqlalchemy import Column, Integer, BigInteger, String

from src.db.database import Base


class Reward(Base):
    __tablename__ = "loyaltypoints"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    points = Column(Integer)
    user_id = Column(String)
    date = Column(BigInteger)


class RewardProducts(Base):
    __tablename__ = "loyaltyitems"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    points = Column(Integer)
    name = Column(String)
    date = Column(BigInteger)
