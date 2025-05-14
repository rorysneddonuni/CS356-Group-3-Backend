from fastapi import FastAPI

from app.database.database import engine, Base
from app.routers.encoders import router as encoders_router
from app.routers.experiments import router as experiments_router
from app.routers.networks import router as networks_router
from app.routers.results import router as results_router
from app.routers.users import router as users_router
from app.routers.videos import router as videos_router

app = FastAPI(title="IKlik Backend Services",
              description="API gateway for dataservices providing data access and management for IKlik services.",
              version="1.0.0", )

app.include_router(encoders_router)
app.include_router(experiments_router)
app.include_router(networks_router)
app.include_router(results_router)
app.include_router(users_router)
app.include_router(videos_router)


@app.on_event("startup")
async def lifespan():
    Base.metadata.create_all(engine)
