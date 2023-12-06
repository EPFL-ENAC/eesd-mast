from fastapi import FastAPI, status, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import config
from app.db import get_session, AsyncSession
from app.services.files.views import router as files_router
from app.services.references.views import router as references_router
from app.services.experiments.views import router as experiments_router
from app.services.runresults.views import router as run_results_router
from pydantic import BaseModel
from sqlalchemy.sql import text

app = FastAPI(root_path=config.PATH_PREFIX)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

@app.get(
    "/healthz",
    tags=["Healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def get_health(
    session: AsyncSession = Depends(get_session),
) -> HealthCheck:
    """
    Endpoint to perform a healthcheck on for kubenernetes liveness and
    readiness probes.
    """
    # Check DB connection
    try:
        await session.exec(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")

    return HealthCheck(status="OK")


app.include_router(
    files_router,
    prefix="/files",
    tags=["Files"],
)
app.include_router(
    references_router,
    prefix="/references",
    tags=["References"],
)
app.include_router(
    experiments_router,
    prefix="/experiments",
    tags=["Experiments"],
)
app.include_router(
    run_results_router,
    prefix="/run_results",
    tags=["Run Results"],
)
