
"""
JWT Authentication ve RBAC (Role-Based Access Control)
"""

import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import bcrypt
import jwt
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
app = FastAPI()

class AuthManager:
    """Hızlı ve güvenli authentication sistemi"""
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key if secret_key is not None else secrets.token_urlsafe(32)
        self.token_expiry = timedelta(hours=24)
        # Demo users (prod'da database'den gelmeli)
        self.users = {
            "admin": {
                "username": "admin",
                "password_hash": self.hash_password("admin123"),
                "roles": ["admin", "user"],
                "permissions": ["*"]
            },
            "user": {
                "username": "user",
                "password_hash": self.hash_password("user123"),
                "roles": ["user"],
                "permissions": ["read", "backup:create", "backup:list"]
            },
            "selamiby": {
                "username": "selamiby",
                "password_hash": self.hash_password("721993by"),
                "roles": ["admin", "user"],
                "permissions": ["*"]
            }
        }

    def hash_password(self, password: str) -> str:
        """Password hash'le"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(errors="ignore")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Password doğrula"""
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            return False

    def create_token(self, username: str, roles: Optional[List[str]] = None) -> str:
        """JWT token oluştur"""
        payload = {
            "sub": username,
            "roles": roles if roles is not None else ["user"],
            "exp": int((datetime.utcnow() + self.token_expiry).timestamp()),
            "iat": int(datetime.utcnow().timestamp())
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Dict:
        """Token doğrula"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token error: {e}")

    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Kullanıcıyı authenticate et"""
        user = self.users.get(username)
        if user and self.verify_password(password, user["password_hash"]):
            return self.create_token(username, user["roles"])
        return None

    def require_role(self, role: str):
        """Role-based authorization decorator"""
        def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
            token = credentials.credentials
            payload = self.verify_token(token)
            if role not in payload.get("roles", []):
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires {role} role"
                )
            return payload
        return role_checker

    def require_permission(self, permission: str):
        """Permission-based authorization decorator"""
        def permission_checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
            token = credentials.credentials
            payload = self.verify_token(token)
            username = payload.get("sub", "")
            user = self.users.get(username) or {}
            user_permissions = user.get("permissions") or []
            if "*" not in user_permissions and permission not in user_permissions:
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires {permission} permission"
                )
            return payload
        return permission_checker

# API Server'da kullanım:
auth_manager = AuthManager()

@app.post("/api/auth/login")
async def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    token = auth_manager.authenticate(username, password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/secure/data")
async def get_secure_data(payload: dict = Depends(auth_manager.require_role("admin"))):
    return {"data": "secure", "user": payload["sub"]}
