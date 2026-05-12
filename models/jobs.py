from sqlalchemy import Column, String, ForeignKey, Integer, Enum, Text, DateTime, func
from database import Base
from uuid import uuid4


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        String,
        unique=True,
        primary_key=True,
        nullable=False,
        default=lambda: str(uuid4()),
    )
    user_id = Column(String, ForeignKey("users.id"), index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    job_type = Column(Enum("FULL_TIME", "PART_TIME", "INTERNSHIP", "CONTRACT"))
    notes = Column(Text, nullable=True)
    current_status = Column(
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
        )
    )
    applied_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
