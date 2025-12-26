"""
Core domain models for AXIOM.

These models represent the essential entities needed for hiring decision calculations.
No database dependencies - pure Python data classes for Phase 1.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class User:
    """
    Represents a user (founder/CEO) of the system.
    
    Attributes:
        id: Unique identifier (optional for Phase 1, will be DB primary key in Phase 2)
        email: User's email address
        name: User's full name
        created_at: Timestamp when user was created
    """
    email: str
    name: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class Company:
    """
    Represents a startup company.
    
    Attributes:
        id: Unique identifier
        name: Company name
        user_id: ID of the user who owns this company
        created_at: Timestamp when company was created
    """
    name: str
    user_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class FinancialSnapshot:
    """
    Represents a point-in-time financial snapshot of the company.
    
    This is the core input for runway calculations.
    
    Attributes:
        id: Unique identifier
        company_id: ID of the company this snapshot belongs to
        current_cash: Current cash balance (in USD)
        monthly_revenue: Monthly recurring revenue (MRR) or average monthly revenue
        monthly_expenses: Total monthly operating expenses (excluding new hire)
        snapshot_date: Date when this snapshot was taken
        created_at: Timestamp when snapshot was created
        
    Assumptions:
        - All amounts are in USD
        - Monthly revenue and expenses are assumed to be constant going forward
        - Current cash is the actual cash on hand at snapshot_date
    """
    company_id: int
    current_cash: Decimal
    monthly_revenue: Decimal
    monthly_expenses: Decimal
    snapshot_date: datetime
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate that amounts are non-negative."""
        if self.current_cash < 0:
            raise ValueError("Current cash cannot be negative")
        if self.monthly_revenue < 0:
            raise ValueError("Monthly revenue cannot be negative")
        if self.monthly_expenses < 0:
            raise ValueError("Monthly expenses cannot be negative")


@dataclass
class HireScenario:
    """
    Represents a potential hiring scenario to evaluate.
    
    Attributes:
        id: Unique identifier
        company_id: ID of the company considering this hire
        role_title: Job title/role name (e.g., "Senior Engineer", "Sales Manager")
        monthly_salary: Base monthly salary (in USD)
        monthly_benefits: Monthly cost of benefits (health insurance, 401k, etc.)
        monthly_overhead: Additional monthly overhead (equipment, software, office space allocation)
        start_date: Proposed start date for this hire
        created_at: Timestamp when scenario was created
        
    Assumptions:
        - All costs are monthly recurring
        - Benefits and overhead are estimated monthly averages
        - No one-time costs (recruiting, onboarding) are included in monthly calculations
        - Start date is informational only for Phase 1
    """
    company_id: int
    role_title: str
    monthly_salary: Decimal
    monthly_benefits: Decimal
    monthly_overhead: Decimal
    start_date: datetime
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate that amounts are non-negative."""
        if self.monthly_salary < 0:
            raise ValueError("Monthly salary cannot be negative")
        if self.monthly_benefits < 0:
            raise ValueError("Monthly benefits cannot be negative")
        if self.monthly_overhead < 0:
            raise ValueError("Monthly overhead cannot be negative")
    
    @property
    def total_monthly_cost(self) -> Decimal:
        """
        Calculate total monthly cost of this hire.
        
        Returns:
            Sum of salary + benefits + overhead
        """
        return self.monthly_salary + self.monthly_benefits + self.monthly_overhead


@dataclass
class HiringImpact:
    """
    Result of evaluating a hiring scenario against a financial snapshot.
    
    Attributes:
        current_runway_months: Current runway before hire (in months)
        new_runway_months: Runway after hire (in months)
        runway_delta_months: Change in runway (negative = shortened, positive = extended)
        current_monthly_burn: Monthly burn rate before hire
        new_monthly_burn: Monthly burn rate after hire
        burn_delta: Change in monthly burn rate
        risk_level: Risk assessment ("Safe", "Risky", "Dangerous")
        
    Assumptions:
        - Runway is calculated assuming constant burn rate
        - Risk levels are based on remaining runway thresholds:
          * Safe: > 12 months remaining
          * Risky: 6-12 months remaining
          * Dangerous: < 6 months remaining
    """
    current_runway_months: Decimal
    new_runway_months: Decimal
    runway_delta_months: Decimal
    current_monthly_burn: Decimal
    new_monthly_burn: Decimal
    burn_delta: Decimal
    risk_level: str
    
    def __post_init__(self):
        """Validate risk level is one of the allowed values."""
        allowed_risk_levels = ["Safe", "Risky", "Dangerous"]
        if self.risk_level not in allowed_risk_levels:
            raise ValueError(f"Risk level must be one of {allowed_risk_levels}")

