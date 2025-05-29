# app/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, utils
from app.database import get_db
from app.config import settings
from typing import Optional
from fastapi.background import BackgroundTasks

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dummy email sender (replace with actual SMTP in prod)
def send_verification_email(email: str, token: str):
    link = f"http://127.0.0.1:8000/auth/verify-email?token={token}"
    print(f"📧 Verification email to {email}: {link}")

@router.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_pw,
        is_ops_user=user.is_ops_user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Generate token & send fake verification email
    token = utils.create_jwt({"user_id": db_user.id})
    background_tasks.add_task(send_verification_email, db_user.email, token)

    # Also return token to frontend (optional)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = utils.decode_jwt(token)
        user_id = payload.get("user_id")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_verified:
            return {"message": "Email already verified"}
        user.is_verified = True
        db.commit()
        return {"message": "Email verified successfully ✅"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not utils.verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    token = utils.create_jwt({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(utils.decode_jwt), db: Session = Depends(get_db)) -> models.User:
    try:
        payload = token
        user = db.query(models.User).filter(models.User.id == payload.get("user_id")).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_verified_user(user: models.User = Depends(get_current_user)):
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    return user

def require_ops_user(user: models.User = Depends(require_verified_user)):
    if not user.is_ops_user:
        raise HTTPException(status_code=403, detail="Only Ops users allowed")
    return user
