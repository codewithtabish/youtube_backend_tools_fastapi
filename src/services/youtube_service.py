from typing import Any

import yt_dlp
from fastapi import HTTPException

from models import YouTubeTagsRequest, YouTubeTagsResponse


class YouTubeService:
    """Service layer for all YouTube related operations"""

    @staticmethod
    async def get_youtube_tags(request: YouTubeTagsRequest) -> YouTubeTagsResponse:
        """
        Extract title and tags from a YouTube video.
        """
        url = request.url.strip()

        # yt-dlp configuration
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {"youtube": {"player_client": ["ios", "web", "android"]}},
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type:ignore
                info: dict[str, Any] = ydl.extract_info(
                    url, download=False
                )  # type:ignore

                title: str = info.get("title", "Untitled Video")
                tags: list[str] = info.get("tags", [])

                # Return properly typed response
                return YouTubeTagsResponse(
                    video_title=title, video_url=url, total_tags=len(tags), tags=tags
                )

        except Exception as exc:
            # Return clean error to the user
            raise HTTPException(
                status_code=500, detail=f"Failed to fetch YouTube tags. Error: {exc!s}"
            ) from exc
