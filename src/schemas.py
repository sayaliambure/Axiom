"""
Pydantic schemas for request/response validation in AXIOM API.

These schemas define the structure of data sent to and received from the API.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List


# ============================================================================
# Authentication Schemas
# ============================================================================

class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (without password)."""
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


# ============================================================================
# Company Schemas
# ============================================================================

class CompanyCreate(BaseModel):
    """Schema for creating a company."""
    name: str = Field(..., min_length=1, max_length=200)


class CompanyResponse(BaseModel):
    """Schema for company response."""
    id: int
    name: str
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Financial Snapshot Schemas
# ============================================================================

class FinancialSnapshotCreate(BaseModel):
    """Schema for creating a financial snapshot."""
    current_cash: Decimal = Field(..., gt=0, description="Current cash balance in USD")
    monthly_revenue: Decimal = Field(..., ge=0, description="Monthly recurring revenue in USD")
    monthly_expenses: Decimal = Field(..., ge=0, description="Monthly operating expenses in USD")
    snapshot_date: datetime = Field(default_factory=datetime.utcnow, description="Date of the snapshot")


class FinancialSnapshotUpdate(BaseModel):
    """Schema for updating a financial snapshot."""
    current_cash: Optional[Decimal] = Field(None, gt=0)
    monthly_revenue: Optional[Decimal] = Field(None, ge=0)
    monthly_expenses: Optional[Decimal] = Field(None, ge=0)
    snapshot_date: Optional[datetime] = None


class FinancialSnapshotResponse(BaseModel):
    """Schema for financial snapshot response."""
    id: int
    company_id: int
    current_cash: Decimal
    monthly_revenue: Decimal
    monthly_expenses: Decimal
    snapshot_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Hire Scenario Schemas
# ============================================================================

class HireScenarioCreate(BaseModel):
    """Schema for creating a hire scenario."""
    role_title: str = Field(..., min_length=1, max_length=200, description="Job title/role name")
    monthly_salary: Decimal = Field(..., ge=0, description="Monthly salary in USD")
    monthly_benefits: Decimal = Field(..., ge=0, description="Monthly benefits cost in USD")
    monthly_overhead: Decimal = Field(..., ge=0, description="Monthly overhead cost in USD")
    start_date: datetime = Field(..., description="Proposed start date for the hire")


class HireScenarioUpdate(BaseModel):
    """Schema for updating a hire scenario."""
    role_title: Optional[str] = Field(None, min_length=1, max_length=200)
    monthly_salary: Optional[Decimal] = Field(None, ge=0)
    monthly_benefits: Optional[Decimal] = Field(None, ge=0)
    monthly_overhead: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[datetime] = None


class HireScenarioResponse(BaseModel):
    """Schema for hire scenario response."""
    id: int
    company_id: int
    role_title: str
    monthly_salary: Decimal
    monthly_benefits: Decimal
    monthly_overhead: Decimal
    start_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Hiring Impact Schemas
# ============================================================================

class HiringImpactResponse(BaseModel):
    """Schema for hiring impact calculation response."""
    current_runway_months: Decimal = Field(..., description="Current runway before hire (months)")
    new_runway_months: Decimal = Field(..., description="Runway after hire (months)")
    runway_delta_months: Decimal = Field(..., description="Change in runway (months)")
    current_monthly_burn: Decimal = Field(..., description="Monthly burn rate before hire")
    new_monthly_burn: Decimal = Field(..., description="Monthly burn rate after hire")
    burn_delta: Decimal = Field(..., description="Change in monthly burn rate")
    risk_level: str = Field(..., description="Risk assessment: Safe, Risky, or Dangerous")
    
    # Include snapshot and scenario info for context
    financial_snapshot: FinancialSnapshotResponse
    hire_scenario: HireScenarioResponse


class HiringImpactRequest(BaseModel):
    """Schema for hiring impact calculation request."""
    financial_snapshot_id: int = Field(..., description="ID of the financial snapshot to use")
    hire_scenario_id: int = Field(..., description="ID of the hire scenario to evaluate")

