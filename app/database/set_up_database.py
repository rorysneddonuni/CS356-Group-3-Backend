from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Experiments(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

class Sample_Video_Storage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    file_path: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.get("/set_up_database")
def on_startup():
    create_db_and_tables()


@app.post("/experiments/")
def create_experiment(experiments: Experiments, session: SessionDep) -> Experiments:
    session.add(experiments)
    session.commit()
    session.refresh(experiments)
    return experiments


@app.get("/experiments/")
def read_experiments(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Experiments]:
    experiments = session.exec(select(Experiments).offset(offset).limit(limit)).all()
    return experiments


@app.get("/experiments/{experiment_id}")
def read_experiment(experiment_id: int, session: SessionDep) -> Experiments:
    experiment = session.get(Experiments, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@app.delete("/experiments/{experiment_id}")
def delete_hero(experiment_id: int, session: SessionDep):
    experiment = session.get(Experiments, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    session.delete(experiment)
    session.commit()
    return {"ok": True}

@app.post("/sampleVideo/")
def create_video(videos: Sample_Video_Storage, session: SessionDep) -> Experiments:
    session.add(videos)
    session.commit()
    session.refresh(videos)
    return videos


@app.get("/sampleVideo/")
def read_video(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Sample_Video_Storage]:
    videos = session.exec(select(Sample_Video_Storage).offset(offset).limit(limit)).all()
    return videos


@app.get("/sampleVideo/{video_id}")
def read_video(video_id: int, session: SessionDep) -> Sample_Video_Storage:
    experiment = session.get(Sample_Video_Storage, video_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Video not found")
    return experiment


@app.delete("/sampleVideo/{video_id}")
def delete_video(video_id: int, session: SessionDep):
    video = session.get(Sample_Video_Storage, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    session.delete(video)
    session.commit()
    return {"ok": True}

