from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(v1_router, prefix="/api/v1", tags=["v1"])

# helth check
@app.get("/health")
async def health():
    return {"status": "ok"}
