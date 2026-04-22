from fastapi import APIRouter

from models import YouTubeTagsRequest, YouTubeTagsResponse
from services import YouTubeService

router = APIRouter(
    prefix="/youtube", tags=["youtube"], responses={404: {"description": "Not found"}}
)


@router.post(
    "/tags",
    response_model=YouTubeTagsResponse,
    summary="Get YouTube Video Tags",
    description="Extract all tags from any YouTube video URL",
)
async def get_youtube_tags(request: YouTubeTagsRequest) -> YouTubeTagsResponse:
    """Get title and all tags of youtube"""
    return await YouTubeService.get_youtube_tags(request=request)
