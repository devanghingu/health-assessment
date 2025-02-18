from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.sql import func


class TimestampMixin:
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())