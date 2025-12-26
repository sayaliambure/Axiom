"""
SQLAlchemy database models for AXIOM.

These models map to database tables and extend the core domain models
from models.py with database-specific functionality.
"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .database import Base


class User(Base):
    """
    Database model for users (founders/CEOs).
    
    Maps to 'users' table in PostgreSQL.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    companies = relationship("Company", back_populates="owner", cascade="all, delete-orphan")


class Company(Base):
    """
    Database model for companies.
    
    Maps to 'companies' table in PostgreSQL.
    """
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="companies")
    financial_snapshots = relationship(
        "FinancialSnapshot",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    hire_scenarios = relationship(
        "HireScenario",
        back_populates="company",
        cascade="all, delete-orphan"
    )


class FinancialSnapshot(Base):
    """
    Database model for financial snapshots.
    
    Maps to 'financial_snapshots' table in PostgreSQL.
    Uses Numeric for precise decimal storage.
    """
    __tablename__ = "financial_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    current_cash = Column(Numeric(15, 2), nullable=False)
    monthly_revenue = Column(Numeric(15, 2), nullable=False)
    monthly_expenses = Column(Numeric(15, 2), nullable=False)
    snapshot_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="financial_snapshots")


class HireScenario(Base):
    """
    Database model for hire scenarios.
    
    Maps to 'hire_scenarios' table in PostgreSQL.
    Uses Numeric for precise decimal storage.
    """
    __tablename__ = "hire_scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role_title = Column(String, nullable=False)
    monthly_salary = Column(Numeric(15, 2), nullable=False)
    monthly_benefits = Column(Numeric(15, 2), nullable=False)
    monthly_overhead = Column(Numeric(15, 2), nullable=False)
    start_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="hire_scenarios")

