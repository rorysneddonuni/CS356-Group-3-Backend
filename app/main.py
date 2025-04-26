from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import yaml

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Get the auto-generated schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    with open("openapi.yaml", "r") as f:
        extension = yaml.safe_load(f)

    openapi_schema.setdefault("tags", []).extend(extension.get("tags", []))
    openapi_schema.setdefault("paths", {}).update(extension.get("paths", {}))
    openapi_schema.setdefault("components", {}).update(extension.get("components", {}))

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
