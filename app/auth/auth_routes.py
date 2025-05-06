

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.core.db import get_db
from app.common.models.exp_users_model import ExpExpressoUser
from app.common.utils.auth_utils import create_access_token, hash_password, verify_password

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/api/auth")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token"""
    result = await db.execute(
        select(ExpExpressoUser).where(
            ExpExpressoUser.email == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": form_data.username, "role": user.role}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
