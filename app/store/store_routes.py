from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.store.store_services import show_hello_world

router = APIRouter(prefix="/store", tags=["Test Routers"])


@router.get("/")
async def show_greeting():
    return await show_hello_world()
