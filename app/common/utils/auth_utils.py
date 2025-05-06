from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

ENDPOINT_ACCESS_RULES = {
    # "/open/": ["OPEN","CUSTOMER","DELIVERY","STORE_EMP","STORE_OWNER","SUPER_ADMIN"],
    "/admin/": ["SUPER_ADMIN"],
    "/store/": ["DELIVERY", "STORE_EMP", "STORE_OWNER", "SUPER_ADMIN"],
    "/cust/": ["CUSTOMER", "DELIVERY", "STORE_EMP", "STORE_OWNER", "SUPER_ADMIN"],
}

# Hash password


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT token


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + \
        (expires_delta if expires_delta else timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Decode JWT token


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        # Debug log
        print(f"[verify_token] username: {username}, role: {role}")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def restrict_users_for(request: Request, user: dict = Depends(verify_token)):
    path = request.url.path

    for endpoint, roles in ENDPOINT_ACCESS_RULES.items():
        if path == endpoint or path.startswith(endpoint.rstrip("/") + "/"):
            if user["role"] in roles:
                return user
            else:
                raise HTTPException(
                    status_code=403, detail="Unauthorized for this path"
                )

    raise HTTPException(status_code=403, detail="Access denied")
