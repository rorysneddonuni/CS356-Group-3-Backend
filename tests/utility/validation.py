from app.models.video import Video


def validate_video(db_obj):
    return Video.model_validate({
        "id": db_obj.id,  # convert int to str if Pydantic expects str
        "title": db_obj.title,
        "path": db_obj.path,
        "format": str(db_obj.format),
        "frameRate": db_obj.frameRate,
        "resolution": str(db_obj.resolution),
        "description": str(db_obj.description),
        "bitDepth": db_obj.bitDepth,
        "createdDate": str(db_obj.createdDate),
        "lastUpdatedBy": str(db_obj.lastUpdatedBy),
    })
