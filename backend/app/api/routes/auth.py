from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, require_interviewer
from app.core.security import create_access_token, hash_password, verify_password
from app.models.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])
user_repository = UserRepository()


def _format_user(user_doc: dict[str, Any]) -> UserResponse:
    return UserResponse(
        id=str(user_doc["_id"]),
        email=user_doc["email"],
        full_name=user_doc.get("full_name", ""),
        role=user_doc.get("role", "candidate"),
        created_at=user_doc.get("created_at"),
    )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(request: UserRegisterRequest):
    existing = await user_repository.get_by_email(request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists",
        )

    pwd_hash = hash_password(request.password)
    user_doc = await user_repository.create_user(
        email=request.email,
        password_hash=pwd_hash,
        full_name=request.full_name,
        role=request.role.value,
    )

    token = create_access_token(
        subject=str(user_doc["_id"]),
        claims={"role": user_doc["role"], "email": user_doc["email"]},
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=_format_user(user_doc),
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest):
    user_doc = await user_repository.get_by_email(request.email)
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(request.password, user_doc.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        subject=str(user_doc["_id"]),
        claims={"role": user_doc["role"], "email": user_doc["email"]},
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=_format_user(user_doc),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict[str, Any] = Depends(get_current_user)):
    return _format_user(current_user)


@router.get(
    "/candidates",
    response_model=list[UserResponse],
    dependencies=[Depends(require_interviewer)],
)
async def list_candidates():
    candidates = await user_repository.list_candidates()
    return [_format_user(c) for c in candidates]
