from typing import List, Optional, Tuple, Union

from fastapi import APIRouter, Form, HTTPException, Path
from pydantic import StrictBytes, StrictStr

from app.models.error import Error
from app.models.video import Video
from app.services.videos import VideosService

router = APIRouter()


@router.post("/infrastructure/videos", responses={200: {"model": Video, "description": "Video created successfully"},
                                                  400: {"model": Error, "description": "Invalid video upload data"},
                                                  415: {"model": Error,
                                                        "description": "Unsupported media type for video upload."},
                                                  422: {"model": Error, "description": "Video file validation error."},
                                                  200: {"model": Error, "description": "Unexpected error"}, },
             tags=["videos"], summary="Create video", response_model_by_alias=True, )
async def create_video(
        video: Optional[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]] = Form(None, description=""),
        frame_rate: Optional[StrictStr] = Form(None, description=""),
        resolution: Optional[StrictStr] = Form(None, description=""), ) -> Video:
    """Upload a new video to the infrastructure portal (Super User access required)."""
    if not VideosService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await VideosService.subclasses[0]().create_video(video, frame_rate, resolution)


@router.delete("/infrastructure/videos/{id}", responses={200: {"model": Video, "description": "Video deleted"},
                                                         404: {"model": Error, "description": "Video not found"},
                                                         200: {"model": Error, "description": "Unexpected error"}, },
               tags=["videos"], summary="Delete video", response_model_by_alias=True, )
async def delete_video(id: StrictStr = Path(..., description=""), ) -> Video:
    """Delete a specific video by ID (Super User access required)."""
    if not VideosService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await VideosService.subclasses[0]().delete_video(id)


@router.get("/infrastructure/videos/{id}", responses={200: {"model": Video, "description": "Video details"},
                                                      404: {"model": Error, "description": "Video not found"},
                                                      200: {"model": Error, "description": "Unexpected error"}, },
            tags=["videos"], summary="Retrieve video", response_model_by_alias=True, )
async def get_video(id: StrictStr = Path(..., description=""), ) -> Video:
    """Fetch a specific video by ID."""
    if not VideosService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await VideosService.subclasses[0]().get_video(id)


@router.get("/infrastructure/videos", responses={200: {"model": List[Video], "description": "A list of videos"},
                                                 200: {"model": Error, "description": "Unexpected error"}, },
            tags=["videos"], summary="Retrieve videos list", response_model_by_alias=True, )
async def get_videos() -> List[Video]:
    """Fetch a list of all available videos."""
    if not VideosService.subclasses:
        raise HTTPException(status_code=501, detail="Not implemented")
    return await VideosService.subclasses[0]().get_videos()
