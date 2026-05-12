from sqlalchemy import ForeignKey, Column, Enum, DateTime, String, Text, func
from uuid import uuid4
from database import Base


class StatusEvent(Base):
    __tablename__ = "status_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"), index=True)
    from_status = Column(
        Enum(
            "WISHLIST",
            "APPLIED",
            "SCREENING",
            "INTERVIEWING",
            "OFFER",
            "ACCEPTED",
            "DECLINED",
            "REJECTED",
            "GHOSTED",
        ),
        nullable=True,
    )
    to_status = Column(
        Enum(
            "WISHLIST",
            "APPLIED",
            "SCREENING",
            "INTERVIEWING",
            "OFFER",
            "ACCEPTED",
            "DECLINED",
            "REJECTED",
            "GHOSTED",
        ),
        nullable=False,
    )
    notes = Column(Text, nullable=True)
    changed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
