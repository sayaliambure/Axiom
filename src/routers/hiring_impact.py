"""
Hiring impact calculation routes.

Uses the financial calculation services from Phase 1 to compute
runway impact of hiring scenarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from ..database import get_db
from ..db_models import User, FinancialSnapshot, HireScenario
from ..schemas import HiringImpactRequest, HiringImpactResponse, FinancialSnapshotResponse, HireScenarioResponse
from ..auth import get_current_user
from ..services import calculate_hiring_impact
from ..models import FinancialSnapshot as DomainFinancialSnapshot, HireScenario as DomainHireScenario

router = APIRouter(prefix="/hiring-impact", tags=["hiring-impact"])


def convert_db_snapshot_to_domain(db_snapshot: FinancialSnapshot) -> DomainFinancialSnapshot:
    """
    Convert database FinancialSnapshot to domain model.
    
    This bridges the database layer with the business logic layer.
    """
    return DomainFinancialSnapshot(
        id=db_snapshot.id,
        company_id=db_snapshot.company_id,
        current_cash=Decimal(str(db_snapshot.current_cash)),
        monthly_revenue=Decimal(str(db_snapshot.monthly_revenue)),
        monthly_expenses=Decimal(str(db_snapshot.monthly_expenses)),
        snapshot_date=db_snapshot.snapshot_date,
        created_at=db_snapshot.created_at
    )


def convert_db_scenario_to_domain(db_scenario: HireScenario) -> DomainHireScenario:
    """
    Convert database HireScenario to domain model.
    
    This bridges the database layer with the business logic layer.
    """
    return DomainHireScenario(
        id=db_scenario.id,
        company_id=db_scenario.company_id,
        role_title=db_scenario.role_title,
        monthly_salary=Decimal(str(db_scenario.monthly_salary)),
        monthly_benefits=Decimal(str(db_scenario.monthly_benefits)),
        monthly_overhead=Decimal(str(db_scenario.monthly_overhead)),
        start_date=db_scenario.start_date,
        created_at=db_scenario.created_at
    )


@router.post("/calculate", response_model=HiringImpactResponse)
def calculate_hiring_impact_endpoint(
    request: HiringImpactRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate the hiring impact on runway.
    
    This endpoint uses the financial calculation services from Phase 1
    to compute how a hire scenario affects the company's runway.
    
    Args:
        request: Request containing financial_snapshot_id and hire_scenario_id
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Hiring impact calculation results including:
        - Current and new runway
        - Runway delta
        - Current and new burn rates
        - Risk assessment
        
    Raises:
        HTTPException: If snapshot or scenario not found or don't belong to user
    """
    # Fetch financial snapshot and verify ownership
    db_snapshot = db.query(FinancialSnapshot).join(
        FinancialSnapshot.company
    ).filter(
        FinancialSnapshot.id == request.financial_snapshot_id,
        FinancialSnapshot.company.has(user_id=current_user.id)
    ).first()
    
    if not db_snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial snapshot not found"
        )
    
    # Fetch hire scenario and verify ownership
    db_scenario = db.query(HireScenario).join(
        HireScenario.company
    ).filter(
        HireScenario.id == request.hire_scenario_id,
        HireScenario.company.has(user_id=current_user.id)
    ).first()
    
    if not db_scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hire scenario not found"
        )
    
    # Verify both belong to the same company
    if db_snapshot.company_id != db_scenario.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Financial snapshot and hire scenario must belong to the same company"
        )
    
    # Convert database models to domain models
    domain_snapshot = convert_db_snapshot_to_domain(db_snapshot)
    domain_scenario = convert_db_scenario_to_domain(db_scenario)
    
    # Calculate hiring impact using Phase 1 services
    # Business logic stays in services.py, not in routes
    impact = calculate_hiring_impact(domain_snapshot, domain_scenario)
    
    # Build response with domain models converted back to response schemas
    return HiringImpactResponse(
        current_runway_months=impact.current_runway_months,
        new_runway_months=impact.new_runway_months,
        runway_delta_months=impact.runway_delta_months,
        current_monthly_burn=impact.current_monthly_burn,
        new_monthly_burn=impact.new_monthly_burn,
        burn_delta=impact.burn_delta,
        risk_level=impact.risk_level,
        financial_snapshot=FinancialSnapshotResponse.model_validate(db_snapshot),
        hire_scenario=HireScenarioResponse.model_validate(db_scenario)
    )

