from datetime import datetime
from typing import Literal
from urllib.parse import parse_qs, urlparse

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

# ===================================================================
# Constants (Fixes Ruff PLR2004 magic number warning)
# ===================================================================
YOUTUBE_VIDEO_ID_LENGTH: int = 11


# ===================================================================
# Base Response Models
# ===================================================================


class ApiResponse(BaseModel):
    """Standard success response used across the API"""

    status: Literal["success"] = "success"
    message: str
    app_name: str = "YouTube Tools API"
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Response timestamp"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "app_name": "YouTube Tools API",
                "timestamp": "2026-04-22T08:30:45.123456",
            }
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response"""

    status: Literal["error"] = "error"
    message: str
    error_code: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "error",
                "message": "Invalid YouTube URL provided",
                "error_code": "INVALID_URL",
                "timestamp": "2026-04-22T08:30:45.123456",
            }
        }
    }


# ===================================================================
# YouTube Specific Models
# ===================================================================


class YouTubeTagsRequest(BaseModel):
    """Request model for extracting YouTube video tags"""

    url: str = Field(
        ...,
        description="YouTube video URL (youtube.com or youtu.be)",
        examples=[
            "https://youtu.be/P6BNvuqYvSA",
            "https://www.youtube.com/watch?v=dQw4w9wgxcQ",
        ],
    )

    model_config = {
        "json_schema_extra": {"example": {"url": "https://youtu.be/P6BNvuqYvSA"}}
    }

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, v: str) -> str:
        """Full validation: domain + video ID must be exactly 11 characters"""
        if not v or not v.strip():
            raise HTTPException(
                status_code=400,
                detail="❌ Please provide a YouTube URL. The 'url' field is required.",
            )

        url = v.strip()
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Allowed YouTube domains
        allowed_domains = {
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "m.youtube.com",
        }

        if domain not in allowed_domains:
            raise HTTPException(
                status_code=400,
                detail="❌ Invalid YouTube URL.Please provide a valid youtube.com or youtu.be link",
            )

        # Extract video ID
        video_id: str | None = None
        if domain == "youtu.be":
            video_id = parsed.path.strip("/")
        elif "v=" in parsed.query:
            video_id = parse_qs(parsed.query).get("v", [None])[0]

        # Video ID must be exactly 11 characters (using constant)
        if not video_id or len(video_id) != YOUTUBE_VIDEO_ID_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"❌ Invalid YouTube video ID {YOUTUBE_VIDEO_ID_LENGTH} characters long.",
            )

        return url  # return cleaned URL


class YouTubeTagsResponse(BaseModel):
    """Response model when YouTube tags are successfully extracted"""

    video_title: str = Field(..., description="Title of the YouTube video")
    video_url: str = Field(..., description="Original YouTube video URL")
    total_tags: int = Field(..., description="Total number of tags")
    tags: list[str] = Field(..., description="List of all tags")

    model_config = {
        "json_schema_extra": {
            "example": {
                "video_title": "Pawan Khera Exclusive Interview",
                "video_url": "https://youtu.be/P6BNvuqYvSA",
                "total_tags": 18,
                "tags": [
                    "pawan khera",
                    "india politics",
                    "assam polls",
                    "exclusive interview",
                ],
            }
        }
    }
