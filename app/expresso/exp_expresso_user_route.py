from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_db
from app.common.schemas.exp_expresso_user_schema import (
    ExpExpressoUserCreate, ExpExpressoUserUpdate, ExpExpressoUserOut
)
from app.expresso.exp_expresso_user_services import (
    create_user, update_user, get_user_by_id, get_all_users
)

router = APIRouter(prefix="/admin", tags=["Expresso Users"])


@router.get("/")
async def get_exp_user_greeting():
    return {"Greeting from admin !!!"}


@router.post("/", response_model=ExpExpressoUserOut)
async def create_exp_user(user: ExpExpressoUserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(user, db)


@router.put("/{user_id}", response_model=ExpExpressoUserOut)
async def update_exp_user(user_id: int, user: ExpExpressoUserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user(user_id, user, db)


@router.get("/{user_id}", response_model=ExpExpressoUserOut)
async def get_exp_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(user_id, db)


@router.get("/", response_model=List[ExpExpressoUserOut])
async def list_exp_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)
