from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.common.models.exp_users_model import ExpExpressoUser
from app.common.schemas.exp_expresso_user_schema import ExpExpressoUserCreate, ExpExpressoUserUpdate
from app.common.utils.password_utils import hash_password, pwd_context


async def create_user(user: ExpExpressoUserCreate, db: AsyncSession):

    new_user = ExpExpressoUser(
        name=user.name,
        email=user.email,
        mobile_number=user.mobile_number,
        role=user.role,
        hashed_password=hash_password(user.password),
        is_active=user.is_active,
        created_by=user.created_by,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(user_id: int, user: ExpExpressoUserUpdate, db: AsyncSession):
    result = await db.execute(select(ExpExpressoUser).where(ExpExpressoUser.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user.dict(exclude_unset=True).items():
        if field == "password":
            setattr(db_user, "password_hash", pwd_context.hash(value))
        else:
            setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(ExpExpressoUser).where(ExpExpressoUser.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(ExpExpressoUser))
    if not result:
        raise HTTPException(status_code=404, detail="No Users")
    return result.scalars().all()
