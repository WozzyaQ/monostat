from sqlalchemy import Column
from sqlalchemy.types import String, BigInteger, VARCHAR, Integer

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class StatementItem(db.Model):
    __tablename__ = 'statement_item'
    id = Column(String, primary_key=True)
    time = Column(BigInteger, nullable=False)
    description = Column(String)
    mcc = Column(Integer)
    originalMcc = Column(Integer)
    amount = Column(Integer, nullable=False)
    operationAmount = Column(Integer)
    currencyCode = Column(Integer)
    commissionRate = Column(Integer)
    cashbackAmount = Column(Integer)
    balance = Column(Integer)
    hold = Column(VARCHAR(5))
    account = Column(String, nullable=False)
