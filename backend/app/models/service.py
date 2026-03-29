import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Text, Numeric, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("businesses.id"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    billing_type: Mapped[str] = mapped_column(String(20), default="one_time")  # one_time, recurring, hourly
    billing_cycle: Mapped[str | None] = mapped_column(String(20), nullable=True)  # weekly, monthly, quarterly, yearly
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)  # hour, session, project, etc.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    business = relationship("Business")
