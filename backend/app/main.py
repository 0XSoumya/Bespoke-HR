import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.auth import router as auth_router
from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.health import router as health_router
from app.api.routes.interview import router as interview_router
from app.api.routes.resume import router as resume_router
from app.core.config.settings import settings
from app.repositories.user_repository import UserRepository

logger = logging.getLogger("ai_interview_system")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    try:
        user_repo = UserRepository()
        await user_repo.ensure_indexes()
        logger.info("Database indexes ensured.")
    except Exception as e:
        logger.warning(f"Could not ensure database indexes: {e}")
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Adaptive AI Interview System API with RAG, adaptive follow-ups, and automated evaluation",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err.get("loc", []))
        errors.append(f"{loc}: {err.get('msg')}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Input validation error",
            "errors": errors,
            "status_code": 422,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "status_code": 500,
        },
    )


# Version 1 API router
from fastapi import APIRouter
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(health_router)
api_v1.include_router(auth_router)
api_v1.include_router(resume_router)
api_v1.include_router(interview_router)
api_v1.include_router(evaluation_router)

app.include_router(api_v1)

# Backwards compatibility / legacy routes (unversioned)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(interview_router)