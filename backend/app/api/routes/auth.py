import base64, hashlib, hmac, json, os, secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest, AuthResponse
from app.services.email_service import send_verification_email, send_reset_email

router = APIRouter(prefix="/auth", tags=["Authentication"])
TOKEN_TTL = int(os.getenv("AUTH_TOKEN_TTL_MINUTES", "60"))
SECRET = os.getenv("AUTH_SECRET", "change-me-in-production")

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 180_000)
    return base64.urlsafe_b64encode(salt + digest).decode()

def verify_password(password: str, stored: str) -> bool:
    try:
        raw = base64.urlsafe_b64decode(stored.encode())
        salt, digest = raw[:16], raw[16:]
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 180_000)
        return hmac.compare_digest(digest, check)
    except Exception:
        return False

def create_token(user: User) -> str:
    payload = {"sub": user.id, "email": user.email, "exp": int((datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL)).timestamp())}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"


def decode_token(token: str):
    try:
        body, sig = token.split(".", 1)
        expected = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected): return None
        padded = body + "=" * (-len(body) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded.encode()))
        if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()): return None
        return payload
    except Exception: return None

def get_current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "", 1) if authorization.startswith("Bearer ") else ""
    payload = decode_token(token)
    if not payload: raise HTTPException(401, "Session expired or invalid")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user: raise HTTPException(401, "User not found")
    return user

def user_dict(user: User):
    return {"id": user.id, "name": user.name, "email": user.email, "is_verified": user.is_verified}

@router.post("/signup", response_model=AuthResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    email = data.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "An account with this email already exists")
    user = User(name=data.name.strip(), email=email, password_hash=hash_password(data.password), verification_token=secrets.token_urlsafe(32))
    db.add(user); db.commit(); db.refresh(user)
    send_verification_email(user.email, user.name, user.verification_token)
    return {"access_token": create_token(user), "user": user_dict(user)}

@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user), "user": user_dict(user)}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user: raise HTTPException(400, "Invalid or expired verification token")
    user.is_verified = True; user.verification_token = None; db.commit()
    return {"message": "Email verified successfully"}

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if user:
        user.reset_token = secrets.token_urlsafe(32)
        user.reset_expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        db.commit(); send_reset_email(user.email, user.name, user.reset_token)
    return {"message": "If an account exists, a password reset email has been sent."}

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == data.token).first()
    if not user or not user.reset_expires_at or user.reset_expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Invalid or expired reset token")
    if len(data.password) < 8: raise HTTPException(400, "Password must be at least 8 characters")
    user.password_hash = hash_password(data.password); user.reset_token = None; user.reset_expires_at = None; db.commit()
    return {"message": "Password reset successfully"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user_dict(user)


@router.post("/refresh", response_model=AuthResponse)
def refresh(user: User = Depends(get_current_user)):
    return {"access_token": create_token(user), "user": user_dict(user)}
