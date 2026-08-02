"""
SQLAlchemy ORM Models

These are INFRASTRUCTURE, not domain entities. Keeping them separate from
app/domain/entities/*.py means the database schema can change (columns,
table names, even swapping ORMs) without the business logic ever knowing.
Repositories translate between these ORM rows and domain entities.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.infrastructure.database.base import Base


class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=True)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("OrderModel", back_populates="client", cascade="all, delete-orphan")


class WebsiteModel(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, unique=True, index=True)
    da_score = Column(Integer, default=0)
    dr_score = Column(Integer, default=0)
    niche = Column(String(255), nullable=True)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("OrderModel", back_populates="website")


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    target_link = Column(String(1000), nullable=False)
    anchor_text = Column(String(255), nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    paid_amount = Column(Float, nullable=False, default=0.0)
    payment_status = Column(String(20), nullable=False, default="unpaid")
    link_status = Column(String(20), nullable=False, default="pending")
    last_checked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("ClientModel", back_populates="orders")
    website = relationship("WebsiteModel", back_populates="orders")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
