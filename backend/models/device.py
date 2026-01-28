from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from models.base import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(String, index=True, nullable=False)
    endpoint = Column(String, unique=True, nullable=False)

    p256dh = Column(String, nullable=False)
    auth = Column(String, nullable=False)

    user_agent = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
