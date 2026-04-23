from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.extensions import Base


class ProductRequest(Base):
    __tablename__ = "product_requests"

    id = Column(Integer, primary_key=True)
    product_name = Column(String(150), nullable=False)
    features = Column(Text, nullable=False)
    platform = Column(String(100), nullable=False)
    tone = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
