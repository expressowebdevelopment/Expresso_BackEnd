from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, func

import enum
from app.core.db import Base
# Enum for role, for now within the model


# class UserRoleEnum(str, enum.Enum):
#     OPEN = "OPEN"
#     CUSTOMER = "CUSTOMER"
#     DELIVERY = "DELIVERY"
#     STORE_EMP = "STORE_EMP"
#     STORE_OWNER = "STORE_OWNER"
#     SUPER_ADMIN = "SUPER_ADMIN"


class ExpExpressoUser(Base):
    __tablename__ = "exp_expresso_users_login"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    mobile_number = Column(String(15), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=True)
    created_on = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_on = Column(DateTime(timezone=True),
                        onupdate=func.now(), nullable=True)

    # is_superuser = Column(Boolean, default=False)  # Optional
    # last_login = Column(DateTime(timezone=True), nullable=True)  # Optional
    # failed_attempts = Column(Integer, default=0)  # Optional
    # locked_until = Column(DateTime(timezone=True), nullable=True)  # Optional
