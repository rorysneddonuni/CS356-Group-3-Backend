from typing import List, Optional

from fastapi import APIRouter
from fastapi import Form, UploadFile
from fastapi.params import Depends, Path, File
from pydantic import StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, FileResponse

from app.auth.dependencies import require_minimum_role
from app.database.database import get_db
from app.models.error import Error
from app.models.user import User
from app.models.video import Video
from app.services.videos import VideosService

router = APIRouter()


@router.post("/infrastructure/videos", responses={200: {"model": Video, "description": "Video created successfully"},
                                                  400: {"model": Error, "description": "Invalid video upload data"},
                                                  415: {"model": Error,
                                                        "description": "Unsupported media type for video upload."},
                                                  422: {"model": Error, "description": "Video file validation error."},
                                                  500: {"model": Error, "description": "Unexpected error"}, },
             tags=["videos"], summary="Create video", response_model_by_alias=True, )
async def create_video(video_file: UploadFile = File(..., description="Video file to upload"),
                       id: Optional[int] = Form(None), groupId: Optional[int] = Form(None),
                       title: Optional[StrictStr] = Form(None), format: Optional[StrictStr] = Form(None),
                       frameRate: Optional[int] = Form(None), res: Optional[StrictStr] = Form(None), description: Optional[StrictStr] = Form(None), bitDepth: Optional[int] = Form(None),
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(require_minimum_role("user"))) -> Video:
    """Upload a new video to the infrastructure portal (Super User access required)."""
    return await VideosService().create_video(video_file, id, groupId, title, format, frameRate, res,description, bitDepth, db)


@router.delete("/infrastructure/videos/{id}", responses={200: {"model": Video, "description": "Video deleted"},
                                                         404: {"model": Error, "description": "Video not found"}},
               tags=["videos"], summary="Delete video", response_model_by_alias=True, )
async def delete_video(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(require_minimum_role("super_admin"))) -> JSONResponse:
    """Delete a specific video by ID (Super User access required)."""
    return await VideosService().delete_video(id, db)


@router.get("/infrastructure/videos/{id}", responses={200: {"model": Video, "description": "Video details"},
                                                      404: {"model": Error, "description": "Video not found"}},
            tags=["videos"], summary="Retrieve video", response_model_by_alias=True, response_class=FileResponse)
async def get_video(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(require_minimum_role("user"))) -> FileResponse:
    """Fetch a specific video by ID."""
    return await VideosService().get_video(id, db)


@router.get("/infrastructure/videos", responses={200: {"model": List[Video], "description": "A list of videos"},
                                                 404: {"description": "No videos found"}}, tags=["videos"],
            summary="Retrieve videos list", response_model_by_alias=True, )
async def get_videos(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_minimum_role("user"))) -> \
        List[Video]:
    """Fetch a list of all available videos."""
    return await VideosService().get_videos(db)
