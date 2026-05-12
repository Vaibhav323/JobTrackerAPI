from fastapi import FastAPI
from auth.router import router as auth_router
from jobs.router import router as job_router
from database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(job_router)
