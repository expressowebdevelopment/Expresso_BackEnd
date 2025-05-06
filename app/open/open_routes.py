from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.open.open_service import show_hello_world
from fastapi import APIRouter
from app.common.schemas.response_schemas import Response
# routes/version.py
from fastapi import APIRouter
from app.common.schemas.versionDTO_schemas import VersionDTO


router = APIRouter(prefix="/open", tags=["Test Routers"])


@router.get("/")
async def show_greeting():
    return await show_hello_world()


@router.get("/plain")
async def show_test():
    return Response(
        success=True,
        message="User fetched successfully",
        data={"id": 1, "name": "John Doe"},
        errors=None
    )


@router.get("/version", response_model=Response[VersionDTO])
def get_version():
    # Hardcoded version info for testing
    version_info = VersionDTO(
        version="1.0.3",
        release_date="2025-05-01",
        build="stable"
    )
    return Response(
        success=True,
        message="Version info fetched successfully",
        data=version_info,
        errors=None
    )
