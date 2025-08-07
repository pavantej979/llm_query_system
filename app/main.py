from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.config import settings

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION
)

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "healthy"}