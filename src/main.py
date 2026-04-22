from typing import Any

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


@app.get("/")
def root() -> Any:
    return {"message": "heelo , i am home route "}


@app.get("/users")
def users() -> Any:
    return {
        "message": "heelo , i am user route ",
        "users": '[{id: 1, "name": "zain"}, {id: 2, "name": "khan"}]',
    }


app.include_router(youtube_router)
