import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routers.encoders import router as encoders_router
from app.routers.experiments import router as experiments_router
from app.routers.networks import router as networks_router
from app.routers.results import router as results_router
from app.routers.users import router as users_router
from app.routers.videos import router as videos_router

from database.database import engine, Base

app = FastAPI(title="IKlik Backend Services",
              description="API gateway for dataservices providing data access and management for IKlik services.",
              version="1.0.0", )

app.include_router(encoders_router)
app.include_router(experiments_router)
app.include_router(networks_router)
app.include_router(results_router)
app.include_router(users_router)
app.include_router(videos_router)


@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#
#     # Get the auto-generated schema
#     openapi_schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes, )
#
#     with open("openapi.yaml", "r") as f:
#         extension = yaml.safe_load(f)
#
#     openapi_schema.setdefault("tags", []).extend(extension.get("tags", []))
#     openapi_schema.setdefault("paths", {}).update(extension.get("paths", {}))
#     openapi_schema.setdefault("components", {}).update(extension.get("components", {}))
#
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
#
# app.openapi = custom_openapi
