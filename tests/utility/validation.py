from app.models.video import Video


def validate_video(db_obj):
    return Video.model_validate({
        "id": db_obj.id,  # convert int to str if Pydantic expects str
        "groupId": db_obj.groupId,  # match exact Pydantic field name
        "title": db_obj.title,
        "path": db_obj.path,
        "format": str(db_obj.format),
        "frameRate": db_obj.frameRate,
        "res": str(db_obj.res),
        "description": str(db_obj.description),
        "bitDepth": db_obj.bitDepth,
        "lastUpdated": str(db_obj.lastUpdated),
    })
