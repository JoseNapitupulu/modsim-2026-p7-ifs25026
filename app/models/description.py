from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from app.extensions import Base


class Description(Base):
    __tablename__ = "descriptions"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    request_id = Column(Integer, ForeignKey("product_requests.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
