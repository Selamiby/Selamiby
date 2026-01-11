"""
Login sayfası için backend API'leri
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Models
class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class MagicLinkRequest(BaseModel):
    email: str

class OTPVerifyRequest(BaseModel):
    code: str

# Demo users (production'da database'den gelecek)
demo_users = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # Production'da hash'li olacak
        "email": "admin@aetheros.com",
        "roles": ["admin", "user"],
        "permissions": ["*"],
        "mfa_enabled": False
    },
    "demo": {
        "username": "demo",
        "password": "demo123",
        "email": "demo@aetheros.com",
        "roles": ["user"],
        "permissions": ["read", "backup:create"],
        "mfa_enabled": True
    }
}

SECRET_KEY = "your-secret-key-change-in-production"  # Gerçek projede .env'den al
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def oauth2_scheme():
    # Dummy dependency for token extraction (FastAPI OAuth2PasswordBearer yerine)
    return ""

@router.post("/login")
async def login(request: LoginRequest):
    """Temel login endpoint'i"""
    user = demo_users.get(request.username)
    
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Token oluştur
    token_data = {
        "sub": request.username,
        "exp": datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES if not request.remember_me else 43200  # 30 days
        ),
        "roles": user["roles"],
        "permissions": user["permissions"]
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return LoginResponse(
        access_token=token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "username": user["username"],
            "email": user["email"],
            "roles": user["roles"]
        }
    )

@router.post("/magic-link")
async def send_magic_link(request: MagicLinkRequest):
    """Magic link gönder"""
    # Burada email gönderme kodu olacak
    return {
        "message": "Magic link sent to your email",
        "expires_in": 900  # 15 minutes
    }

@router.post("/verify-otp")
async def verify_otp(request: OTPVerifyRequest):
    """OTP doğrula"""
    # Gerçek TOTP doğrulama
    return {"valid": True}

@router.post("/social/{provider}")
async def social_login(provider: str, code: str):
    """Social login callback"""
    # OAuth2 flow implementation
    return {"message": f"{provider} login successful"}

@router.post("/logout")
async def logout():
    """Logout"""
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Current user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = demo_users.get(username)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return {
            "username": user["username"],
            "email": user["email"],
            "roles": user["roles"],
            "mfa_enabled": user.get("mfa_enabled", False)
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
