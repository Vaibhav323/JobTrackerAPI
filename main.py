from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from jobs.router import router as job_router
from database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(job_router)

origins = [
    "http://localhost:3000",  # React frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
