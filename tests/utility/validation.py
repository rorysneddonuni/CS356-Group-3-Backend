from app.models.video import Video


def validate_video(db_obj):
    return Video.model_validate({
        "id": db_obj.id,  # convert int to str if Pydantic expects str
        "groupId": db_obj.groupId,  # match exact Pydantic field name
        "filename": db_obj.filename,
        "path": db_obj.path,
        "video_type": str(db_obj.video_type),
        "frame_rate": db_obj.frame_rate,
        "resolution": str(db_obj.resolution),
        "created_date": str(db_obj.created_date),
    })
