import json

from app.database.tables.videos import InputVideo
from app.models.experiment import Experiment
from app.models.video import Video


def validate_experiment(db_obj):
    return Experiment.model_validate({
        "id": db_obj.id,
        "experiment_name": db_obj.experiment_name,  # match exact Pydantic field name
        "description": db_obj.description,
        "owner_id": db_obj.owner_id,
        "status": db_obj.status,
        "video_sources": json.loads(db_obj.video_sources) if db_obj.video_sources else [],
        "encoding_parameters": json.loads(db_obj.encoding_parameters) if db_obj.encoding_parameters else {},
        "network_disruption_profile_id": db_obj.network_disruption_profile_id,
        "metrics_requested": json.loads(db_obj.metrics_requested) if db_obj.metrics_requested else [],
        "created_at": db_obj.created_at.isoformat() if db_obj.created_at else None,
        "network_disruption_profile": db_obj.network_disruption_profile,
    })

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

def validate_encoder(db_obj):
    return Video.model_validate({
        "id": db_obj.id,  # convert int to str if Pydantic expects str
        "name": db_obj.name,  # match exact Pydantic field name
        "type": db_obj.type,
        "comment": db_obj.comment,
        "scalable": str(db_obj.scalable),
        "noOfLayers": str(db_obj.noOfLayers),
        "path": db_obj.path,
        "filename": db_obj.fileName,
        "modeFileReq": str(db_obj.modeFileReq),
        "seqFileReq": str(db_obj.seqFileReq),
        "layersFileReq": str(db_obj.layersFileReq),
    })