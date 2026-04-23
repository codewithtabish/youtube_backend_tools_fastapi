from typing import Any, Optional
import yt_dlp
from fastapi import HTTPException

from models import YouTubeTagsRequest, YouTubeTagsResponse


class YouTubeService:
    """Service layer for YouTube related operations"""

    COOKIES_PATH: Optional[str] = "cookies.txt"

    @staticmethod
    async def get_youtube_tags(request: YouTubeTagsRequest) -> YouTubeTagsResponse:
        url = request.url.strip()

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {
                "youtube": {
                    # 🔥 These player clients return full tags reliably
                    "player_client": [
                        "web_safari",
                        "ios",
                        "android",
                        "web",
                        "web_creator",
                    ],
                }
            },
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "cookies": YouTubeService.COOKIES_PATH,
            "allow_unplayable_formats": True,
            "ignore_no_formats_error": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type:ignore
                info: dict[str, Any] = ydl.extract_info(
                    url, download=False
                )  # type:ignore

                title: str = info.get("title", "Untitled Video")
                tags: list[str] = info.get("tags", [])

                return YouTubeTagsResponse(
                    video_title=title,
                    video_url=url,
                    total_tags=len(tags),
                    tags=tags,
                )

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch YouTube tags. Error: {exc!s}",
            ) from exc
