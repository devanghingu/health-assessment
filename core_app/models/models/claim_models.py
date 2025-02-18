from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime
from core_app.models.database import Base
from .timestamp_modes import TimestampMixin


class Claim(Base, TimestampMixin):
    __tablename__ = "Claim"

    id = Column(Integer, primary_key=True, index=True)
    submitted_procedure = Column(String(7), nullable=False)
    quadrant = Column(String(10), nullable=True)
    plan_group = Column(String)
    subscriber = Column(BigInteger)
    provider_npi = Column(BigInteger)
    provider_fees = Column(Float)
    allowed_fees = Column(Float)
    member_coinsurance = Column(Float,default=0)
    member_copay = Column(Float,default=0)
    net_fee = Column(Float,default=0,nullable=True)
    service_date = Column(DateTime)

    def __repr__(self):
        return (f"PG - {self.plan_group}, SP - {self.submitted_procedure} subscriber {self.subscriber} "
                f"net Fee {self.net_fee}")
