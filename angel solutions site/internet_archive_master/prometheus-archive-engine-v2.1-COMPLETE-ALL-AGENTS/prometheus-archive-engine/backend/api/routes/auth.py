"""
Prometheus Archive Engine - Account Authentication Router
Provides signup, login, refresh, profile management, and audit log lookups
"""
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_db
from ...core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user
)
from ...models.database import User, SubscriptionPlan, AuditLog

router = APIRouter()

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def log_system_event(db: AsyncSession, user_id: str, action: str, request: Request, details: dict = None):
    """Log audit trail events asynchronously"""
    import asyncio
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("User-Agent", "unknown")
    audit = AuditLog(
        id=str(uuid4()),
        user_id=user_id,
        action=action,
        ip_address=ip,
        user_agent=ua,
        details=details
    )
    db.add(audit)

@router.post("/register", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_account(payload: UserRegisterSchema, request: Request, db: AsyncSession = Depends(get_db)):
    """Creates a new user profile and triggers dynamic quota plan builder"""
    # Check if email is already taken
    existing_user_result = await db.execute(select(User).filter(User.email == payload.email))
    if existing_user_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this email already registered"
        )

    user_id = str(uuid4())
    hashed_pwd = hash_password(payload.password)

    # Instantiate new User
    user = User(
        id=user_id,
        email=payload.email,
        password_hash=hashed_pwd,
        role="user",
        subscription_tier="free"
    )
    db.add(user)

    # Build associated SubscriptionPlan with free quotas
    sub_plan = SubscriptionPlan(
        id=str(uuid4()),
        user_id=user_id,
        plan_name="free",
        is_active=False,
        archives_used=0,
        archives_limit=50,
        ai_queries_used=0,
        ai_queries_limit=10,
        storage_used_mb=0.0,
        storage_limit_mb=500.0
    )
    db.add(sub_plan)

    # Log action inside audit records
    log_system_event(db, user_id, "account_registration", request, {"email": payload.email})
    await db.commit()

    # Real-time sync to Base44
    try:
        from ...core.base44_sync import sync_to_base44
        await sync_to_base44("User", {
            "id": user_id,
            "email": payload.email,
            "role": "user",
            "subscription_tier": "free",
            "password_hash": hashed_pwd
        })
        await sync_to_base44("SubscriptionPlan", {
            "id": sub_plan.id,
            "user_id": user_id,
            "plan_name": "free",
            "is_active": False,
            "archives_used": 0,
            "archives_limit": 50,
            "ai_queries_used": 0,
            "ai_queries_limit": 10,
            "storage_used_mb": 0.0,
            "storage_limit_mb": 500.0,
            "created_by_id": user_id
        })
    except Exception as sync_exc:
        from ...core.base44_sync import logger as sync_logger
        sync_logger.error(f"Failed to sync user/plan to Base44 on registration: {sync_exc}")

    # Create active session credentials
    data_payload = {"sub": user_id, "tier": "free", "role": "user"}
    access = create_access_token(data_payload)
    refresh = create_refresh_token(data_payload)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

@router.post("/login", response_model=TokenResponseSchema)
async def login_account(payload: UserLoginSchema, request: Request, db: AsyncSession = Depends(get_db)):
    """Verifies account credentials and yields active token pairs"""
    result = await db.execute(select(User).filter(User.email == payload.email))
    user = result.scalars().first()
    
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account email or password"
        )

    # Create active session credentials
    data_payload = {"sub": user.id, "tier": user.subscription_tier, "role": user.role}
    access = create_access_token(data_payload)
    refresh = create_refresh_token(data_payload)

    log_system_event(db, user.id, "account_login", request)
    await db.commit()

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

@router.get("/me")
async def get_user_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Retrieve full detail maps for currently active user sessions"""
    plan_result = await db.execute(select(SubscriptionPlan).filter(SubscriptionPlan.user_id == current_user.id))
    plan = plan_result.scalars().first()

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "subscription_tier": current_user.subscription_tier,
        "created_at": current_user.created_at,
        "quota": {
            "archives_used": plan.archives_used if plan else 0,
            "archives_limit": plan.archives_limit if plan else 50,
            "ai_queries_used": plan.ai_queries_used if plan else 0,
            "ai_queries_limit": plan.ai_queries_limit if plan else 10,
            "storage_used_mb": plan.storage_used_mb if plan else 0.0,
            "storage_limit_mb": plan.storage_limit_mb if plan else 500.0,
        }
    }
