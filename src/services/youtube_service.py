from typing import Any
import random

import yt_dlp
from fastapi import HTTPException

from models import YouTubeTagsRequest, YouTubeTagsResponse


class YouTubeService:
    """Improved service with better anti-bot protection"""

    @staticmethod
    async def get_youtube_tags(request: YouTubeTagsRequest) -> YouTubeTagsResponse:
        url = request.url.strip()

        # Multiple strategies to reduce bot detection
        ydl_opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {
                "youtube": {
                    "player_client": [
                        "ios",
                        "android",
                        "web",
                        "web_creator",
                        "web_embedded",
                    ],
                    "impersonate": random.choice(
                        ["chrome-124", "chrome-120", "safari-17"]
                    ),
                }
            },
            "http_headers": {
                "User-Agent": random.choice(
                    [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                    ]
                ),
                "Accept-Language": "en-US,en;q=0.9",
            },
            "extractor_retries": 3,
            "sleep_requests": 1,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type:ignore
                info = ydl.extract_info(url, download=False)

                title: str = info.get("title", "Untitled Video")  # type:ignore
                tags: list[str] = info.get("tags", [])  # type:ignore

                return YouTubeTagsResponse(
                    video_title=title,
                    video_url=url,
                    total_tags=len(tags),
                    tags=tags,
                )

        except Exception as exc:
            error = str(exc)
            if "Sign in to confirm you’re not a bot" in error:
                raise HTTPException(
                    status_code=429,
                    detail="YouTube is temporarily blocking this video. Please try again in a few minutes.",
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to fetch YouTube tags. Please try again later.",
                ) from exc
