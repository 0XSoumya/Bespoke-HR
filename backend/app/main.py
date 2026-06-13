from fastapi import FastAPI

from app.api.routes.health import (
    router as health_router,
)

from app.api.routes.resume import (
    router as resume_router,
)

from app.api.routes.interview import (
    router as interview_router,
)

app = FastAPI(
    title="AI Interview System"
)

app.include_router(
    health_router
)

app.include_router(
    resume_router
)

app.include_router(
    interview_router
)