"""
Prometheus Archive Engine - Database Models
SQLAlchemy 2.0 Async Models
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models"""
    pass

class User(Base):
    """User account entity"""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="user", nullable=False) # admin, user
    subscription_tier: Mapped[str] = mapped_column(String(32), default="free", nullable=False) # free, pro, enterprise
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(128), unique=True, nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(128), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    subscription_plan: Mapped["SubscriptionPlan"] = relationship("SubscriptionPlan", back_populates="user", uselist=False, cascade="all, delete-orphan")
    collections: Mapped[List["Collection"]] = relationship("Collection", back_populates="creator", cascade="all, delete-orphan")
    archives: Mapped[List["ArchivedContent"]] = relationship("ArchivedContent", back_populates="creator", cascade="all, delete-orphan")
    searches: Mapped[List["SearchHistory"]] = relationship("SearchHistory", back_populates="creator", cascade="all, delete-orphan")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

class SubscriptionPlan(Base):
    """Active subscription status, limits, and resource meter"""
    __tablename__ = "subscription_plans"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    plan_name: Mapped[str] = mapped_column(String(32), default="free", nullable=False) # free, pro, enterprise
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Usage quotas
    archives_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    archives_limit: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    ai_queries_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ai_queries_limit: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    storage_used_mb: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    storage_limit_mb: Mapped[float] = mapped_column(Float, default=500.0, nullable=False)
    
    billing_cycle_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    billing_cycle_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="subscription_plan")

class Collection(Base):
    """User groupings of archived items"""
    __tablename__ = "collections"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(16), default="#2563eb", nullable=False) # RJ Blue Default
    icon: Mapped[str] = mapped_column(String(32), default="folder", nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    item_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_by_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    creator: Mapped["User"] = relationship("User", back_populates="collections")
    items: Mapped[List["ArchivedContent"]] = relationship("ArchivedContent", back_populates="collection")

class ArchivedContent(Base):
    """References to saved items from the Internet Archive"""
    __tablename__ = "archived_contents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True) # Internet Archive identifier
    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[str] = mapped_column(String(32), default="webpage", nullable=False) # webpage, book, game, software, apk
    snapshot_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # Comma-separated
    collection_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("collections.id", ondelete="SET NULL"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False) # pending, archived, failed, processing
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    archive_source: Mapped[str] = mapped_column(String(32), default="manual", nullable=False) # manual, wayback, ai_agent, bulk_import
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    creator: Mapped["User"] = relationship("User", back_populates="archives")
    collection: Mapped[Optional["Collection"]] = relationship("Collection", back_populates="items")

class SearchHistory(Base):
    """User query logs"""
    __tablename__ = "search_histories"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    search_type: Mapped[str] = mapped_column(String(32), default="web", nullable=False) # wayback, web, ai_research, domain, books, games, software, apk
    results_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    results_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relations
    creator: Mapped["User"] = relationship("User", back_populates="searches")

class AuditLog(Base):
    """System-wide transaction and trace tracking logs"""
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False) # login, logout, create_archive, stripe_charge, rebrand_start, rebrand_finish
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")
