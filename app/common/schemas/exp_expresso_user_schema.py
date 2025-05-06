from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


# class UserRoleEnum(str, Enum):
#     OPEN = "OPEN"
#     CUSTOMER = "CUSTOMER"
#     DELIVERY = "DELIVERY"
#     STORE_EMP = "STORE_EMP"
#     STORE_OWNER = "STORE_OWNER"
#     SUPER_ADMIN = "SUPER_ADMIN"


class ExpExpressoUserBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    role: str
    is_active: Optional[bool] = True


class ExpExpressoUserCreate(ExpExpressoUserBase):
    password: str
    created_by: int


class ExpExpressoUserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    mobile_number: Optional[str]
    password: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]
    updated_by: int


class ExpExpressoUserOut(ExpExpressoUserBase):
    id: int
    created_on: datetime
    updated_on: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
