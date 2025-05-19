from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.database.database import engine, Base
from app.routers.encoders import router as encoders_router
from app.routers.experiments import router as experiments_router
from app.routers.networks import router as networks_router
from app.routers.results import router as results_router
from app.routers.users import router as users_router
from app.routers.videos import router as videos_router
from app.routers.auth import router as auth_router

app = FastAPI(title="IKlik Backend Services",
              description="API gateway for dataservices providing data access and management for IKlik services.",
              version="1.0.0")

app.include_router(encoders_router)
app.include_router(experiments_router)
app.include_router(networks_router)
app.include_router(results_router)
app.include_router(users_router)
app.include_router(videos_router)
app.include_router(auth_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Custom OpenAPI schema to enable JWT auth in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    EXCLUDE_PATHS = ["/auth/login"]

    for path, path_item in openapi_schema["paths"].items():
        if path in EXCLUDE_PATHS:
            continue
        for operation in path_item.values():
            operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
