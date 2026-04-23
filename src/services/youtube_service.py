from typing import Any, Optional
import random
import yt_dlp
from fastapi import HTTPException

from models import YouTubeTagsRequest, YouTubeTagsResponse


class YouTubeService:
    """Service layer for YouTube related operations"""

    # 🧠 Works for FREE tier (list of proxies)
    PROXIES = [
        "http://zovtbsev:qadh4cbyql1g@31.59.20.176:6754",
        "http://zovtbsev:qadh4cbyql1g@198.23.239.134:6540",
        "http://zovtbsev:qadh4cbyql1g@45.38.107.97:6014",
        "http://zovtbsev:qadh4cbyql1g@107.172.163.27:6543",
        "http://zovtbsev:qadh4cbyql1g@198.105.121.200:6462",
        "http://zovtbsev:qadh4cbyql1g@216.10.27.159:6837",
        "http://zovtbsev:qadh4cbyql1g@142.111.67.146:5611",
        "http://zovtbsev:qadh4cbyql1g@191.96.254.138:6185",
        "http://zovtbsev:qadh4cbyql1g@31.58.9.4:6077",
        "http://zovtbsev:qadh4cbyql1g@104.239.107.47:5699",
    ]

    # 💰 For PAID tier (single gateway)
    PAID_PROXY: Optional[str] = None
    # Example:
    # PAID_PROXY = "http://username:password@gateway.webshare.io:port"

    @staticmethod
    def _get_proxy() -> Optional[str]:
        """
        Decide which proxy system to use:
        - Paid proxy (preferred if set)
        - otherwise free random proxy
        """
        if YouTubeService.PAID_PROXY:
            return YouTubeService.PAID_PROXY

        if YouTubeService.PROXIES:
            return random.choice(YouTubeService.PROXIES)

        return None

    @staticmethod
    async def get_youtube_tags(request: YouTubeTagsRequest) -> YouTubeTagsResponse:
        url = request.url.strip()

        proxy = YouTubeService._get_proxy()

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
            "http_headers": {
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "en-US,en;q=0.9",
            },
        }

        # 🔥 add proxy only if exists
        if proxy:
            ydl_opts["proxy"] = proxy  # type:ignore

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
