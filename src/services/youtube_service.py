from typing import Any, Optional
import random
import yt_dlp
from fastapi import HTTPException

from models import YouTubeTagsRequest, YouTubeTagsResponse


class YouTubeService:
    """Service layer for all YouTube related operations"""

    # 🔥 COOKIES (very important for good results)
    COOKIES_PATH: Optional[str] = "cookies.txt"

    # 🔥 YOUR DECODO FREE TRIAL PROXY
    DECODO_USERNAME = "sprf868gvw"
    DECODO_PASSWORD = "hdtm8~oj9eqiSB9F5O"
    DECODO_PORTS = list(range(10001, 10011))  # 10001 to 10010

    @staticmethod
    def _get_proxy() -> str:
        """Return random Decodo proxy each time"""
        port = random.choice(YouTubeService.DECODO_PORTS)
        return (
            f"http://{YouTubeService.DECODO_USERNAME}:"
            f"{YouTubeService.DECODO_PASSWORD}@"
            f"gate.decodo.com:{port}"
        )

    @staticmethod
    async def get_youtube_tags(request: YouTubeTagsRequest) -> YouTubeTagsResponse:
        """
        Extract title and tags from a YouTube video.
        """
        url = request.url.strip()

        # yt-dlp configuration with proxy + cookies
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            # "extractor_args": {
            #     "youtube": {
            #         "player_client": [
            #             "web_safari",
            #             "ios",
            #             "android",
            #             "web",
            #             "web_creator",
            #         ],
            #     }
            # },
            # "cookies": YouTubeService.COOKIES_PATH,
            "proxy": YouTubeService._get_proxy(),  # ← Proxy added here
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
