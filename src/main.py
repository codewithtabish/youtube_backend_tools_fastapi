from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import youtube_router

app: FastAPI = FastAPI(
    title="Youtube Tools",
    description="Backend API for YouTube Tags & Download",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(youtube_router)
