from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.db.session import Base, engine

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(router, prefix="/api", tags=["engineering-docs"])


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
