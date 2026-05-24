from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from starlette import status
from typing import Optional
from enum import Enum
import datetime as dt

# Local Import
from database import db_dependency
from auth.utils import AuthDependency, get_current_user
from models import Job, StatusEvent

router = APIRouter()


class JobType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_ITME = "PART_TIME"
    INTERNSHIP = "INTERNSHIP"
    CONTRACT = "CONTRACT"


class JobStatusType(str, Enum):
    WISHLIST = "WISHLIST"
    APPLIED = "APPLIED"
    SCRRENING = "SCREENING"
    INTERVIEWING = "INTERVIEWING"
    OFFER = "OFFER"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    REJECTED = "REJECTED"
    GHOSTED = "GHOSTED"


class JobCreate(BaseModel):
    title: str
    company: str
    job_type: JobType
    url: Optional[HttpUrl] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: Optional[str] = None
    applied_at: Optional[dt.datetime] = None

    model_config = {"from_attributes": True}


class FetchJob(BaseModel):
    status: JobStatusType = None
    company: str = None
    job_type: JobType = None
    search: str = None
    page: int = 1
    limit: int = 20


class JobCreateResponse(BaseModel):
    user_id: str
    title: str
    company: str
    job_type: JobType
    url: Optional[HttpUrl] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    notes: Optional[str] = None
    applied_at: Optional[dt.datetime] = None
    current_status: JobStatusType
    applied_at: dt.datetime
    # created_at: dt.datetime
    # updated_at: dt.datetime
    model_config = {"from_attributes": True}


@router.post(
    "/api/v1/jobs",
    tags=["Jobs"],
    response_model=JobCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    db: db_dependency, job_create_request: JobCreate, token=Depends(AuthDependency)
):
    initial_stauts = "WISHLIST" if not job_create_request.applied_at else "APPLIED"
    current_user_id = get_current_user(db=db, token=token)
    try:
        new_job = Job(
            user_id=current_user_id,
            title=job_create_request.title,
            company=job_create_request.company,
            job_type=job_create_request.job_type,
            url=str(job_create_request.url),
            location=job_create_request.location,
            salary_min=job_create_request.salary_min,
            salary_max=job_create_request.salary_max,
            notes=job_create_request.notes,
            applied_at=job_create_request.applied_at,
            current_status=initial_stauts,
        )
        db.add(new_job)

        new_status = StatusEvent(
            job=new_job,
            from_status=None,
            to_status=initial_stauts,
            changed_at=dt.datetime.now(dt.timezone.utc),
        )
        db.add(new_status)
        db.commit()
        db.refresh(new_job)

        db.refresh(new_status)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}"
        )
    else:
        return new_job


@router.get("/api/v1/jobs", tags=["Jobs"], status_code=status.HTTP_200_OK)
async def fetch_jobs(
    db: db_dependency, show_jobs: FetchJob, token=Depends(AuthDependency)
):
    pass


@router.get("/api/v1/jobs/{job_id}", tags=["Jobs"], status_code=status.HTTP_200_OK)
async def fetch_job(
    db: db_dependency, token=Depends(AuthDependency), job_id: int = None
):
    pass


@router.patch("/api/v1/jobs/{job_id}", tags=["Jobs"], status_code=status.HTTP_200_OK)
async def update_job(
    db: db_dependency, token=Depends(AuthDependency), job_id: int = None
):
    pass


@router.delete(
    "/api/v1/jobs/{job_id}", tags=["Jobs"], status_code=status.HTTP_204_NO_CONTENT
)
async def delete_job(
    db: db_dependency, token=Depends(AuthDependency), job_id: int = None
):
    pass


# Status Endpoints
@router.post(
    "/api/v1/jobs/{job_id}/status",
    tags=["Status"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create_status(
    db: db_dependency, token=Depends(AuthDependency), job_id: int = None
):
    pass


@router.post(
    "/api/v1/jobs/{job_id}/timeline",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Status"],
)
async def create_timeline(
    db: db_dependency, token=Depends(AuthDependency), job_id: int = None
):
    pass
