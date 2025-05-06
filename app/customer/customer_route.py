from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.customer.customer_services import show_hello_world_from_customer

router = APIRouter(prefix="/cust", tags=["Customer Routers"])


@router.get("/")
async def customer_greeting():
    return await show_hello_world_from_customer()
