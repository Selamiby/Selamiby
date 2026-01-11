from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_users_db = {
    "demo@nexus.com": {
        "email": "demo@nexus.com",
        "hashed_password": "demo123",
        "invite": "NEXUS2026",
        "plan": "free"
    }
}

class User(BaseModel):
    email: str
    plan: str

class UserInDB(User):
    hashed_password: str
    invite: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    invite: str
    plan: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/register")
def register(req: RegisterRequest):
    if req.invite != "NEXUS2026":
        raise HTTPException(status_code=400, detail="Geçersiz davet kodu!")
    if req.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı!")
    fake_users_db[req.email] = {
        "email": req.email,
        "hashed_password": req.password,
        "invite": req.invite,
        "plan": req.plan
    }
    return {"message": f"{req.plan.capitalize()} kayıt başarılı!"}

@app.post("/api/login")
def login(req: LoginRequest):
    user = fake_users_db.get(req.email)
    if not user or user["hashed_password"] != req.password:
        raise HTTPException(status_code=400, detail="Geçersiz e-posta veya şifre!")
    return {"message": "Giriş başarılı!", "plan": user["plan"]}

@app.get("/api/user")
def get_user(email: str):
    user = fake_users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı!")
    return {"email": user["email"], "plan": user["plan"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
