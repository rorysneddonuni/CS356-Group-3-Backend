from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routers.encoders import router as encoders_router
from app.routers.experiments import router as experiments_router
from app.routers.networks import router as networks_router
from app.routers.results import router as results_router
from app.routers.users import router as users_router
from app.routers.videos import router as videos_router
import yaml
from contextlib import asynccontextmanager

from app.database.tables.user import router as user_router

app = FastAPI(title="IKlik Backend Services",
              description="API gateway for dataservices providing data access and management for IKlik services.",
              version="1.0.0", )

app.include_router(encoders_router)
app.include_router(experiments_router)
app.include_router(networks_router)
app.include_router(results_router)
app.include_router(users_router)
app.include_router(videos_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: create tables
    from app.database.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # 1) generate the base schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # 2) load your extension file
    with open("openapi.yaml", "r") as f:
        extension = yaml.safe_load(f)

    # 3) helper for deep merging two dicts
    def deep_merge(dest: dict, src: dict):
        for key, val in src.items():
            if (
                key in dest
                and isinstance(dest[key], dict)
                and isinstance(val, dict)
            ):
                deep_merge(dest[key], val)
            else:
                dest[key] = val

    # 4) merge tags, paths, components deeply
    if ext_tags := extension.get("tags"):
        openapi_schema.setdefault("tags", []).extend(ext_tags)

    if ext_paths := extension.get("paths"):
        deep_merge(openapi_schema.setdefault("paths", {}), ext_paths)

    if ext_comps := extension.get("components"):
        deep_merge(openapi_schema.setdefault("components", {}), ext_comps)

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

def start():
    """Start the FastAPI server with reload for local development."""
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    start()
