import os
from datetime import datetime
from typing import List
from typing import Optional, ClassVar, Tuple

from fastapi import HTTPException, UploadFile
from pydantic import StrictStr
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse, FileResponse

from app.database.tables.videos import InputVideo as input_video_table
from app.models.video import Video
from tests.utility.validation import validate_video

now = datetime.now()
path = "app\database\\videos"

from app.services.utility.video_file_handler import delete_video_file, store_video_file


class VideosService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        VideosService.subclasses = VideosService.subclasses + (cls,)

    async def create_video(self, video: UploadFile, id: Optional[int], groupId: Optional[int],
                           title: Optional[StrictStr], format: Optional[StrictStr], frameRate: Optional[int],
                           res: Optional[StrictStr], description: Optional[StrictStr], bitDepth: Optional[int], db) -> Video:
        """Upload a new video to the infrastructure portal (Super User access required)."""

        result = await db.execute(select(input_video_table).where(or_(input_video_table.id == id)))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(status_code=400, detail="Video already exists")

        if not bitDepth == 8 and not bitDepth == 12:
            raise HTTPException(status_code=400, detail="BitDepth must be either 8 or 12")

        if not format == "yuv" and not format == "y4m":
            raise HTTPException(status_code=400, detail="Accepted formats are: yuv, y4m")

        # Create and save experiment
        data = {"id": id, "groupId": groupId, "title": title, "path": path, "format": format,
                "frameRate": frameRate, "res": res, "description": description, "bitDepth": bitDepth, "lastUpdated": now.strftime("%m/%d/%Y, %H:%M:%S")}

        db_obj = input_video_table(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        store_video_file(video.file, path, data["title"] + "." + data["format"])
        return validate_video(db_obj)

    async def delete_video(self, video_id: StrictStr, db) -> JSONResponse:
        """Delete a specific video by ID (Super User access required)."""
        db_obj = await db.execute(select(input_video_table).filter(input_video_table.id == video_id))
        video_info = db_obj.scalars().first()
        file = video_info.path + "\\" + video_info.title

        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")

        delete_video_file(file)

        await db.delete(video_info)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Video deleted"})

    async def get_video(self, video_id: StrictStr, db: AsyncSession):
        """Fetch a specific video by ID."""
        # todo user authentication
        db_obj = await db.execute(select(input_video_table).filter(input_video_table.id == video_id))
        video_info = db_obj.scalars().first()
        path = video_info.path
        file = video_info.title
        format = video_info.format
        file_path = path + "\\" + file + "." + format

        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")

        if not file_path:
            raise HTTPException(status_code=404, detail="No video files found")

        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Error Retrieving File")
        return FileResponse(path=file_path, media_type=video_info.format, filename=file)

    async def get_videos(self, db) -> List[Video]:
        """Fetch a list of all available videos."""
        db_obj = await db.execute(select(input_video_table))
        all_videos = db_obj.scalars()

        if not all_videos:
            raise HTTPException(status_code=404, detail="No videos found")

        return all_videos
