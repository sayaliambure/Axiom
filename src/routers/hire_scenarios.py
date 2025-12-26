"""
Hire scenario CRUD routes.

All operations are scoped to the user's companies.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..db_models import User, Company, HireScenario
from ..schemas import (
    HireScenarioCreate,
    HireScenarioUpdate,
    HireScenarioResponse
)
from ..auth import get_current_user
from .financial_snapshots import verify_company_access

router = APIRouter(prefix="/hire-scenarios", tags=["hire-scenarios"])


@router.post("", response_model=HireScenarioResponse, status_code=status.HTTP_201_CREATED)
def create_hire_scenario(
    scenario_data: HireScenarioCreate,
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new hire scenario for a company.
    
    Args:
        scenario_data: Hire scenario data
        company_id: ID of the company
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created hire scenario
        
    Raises:
        HTTPException: If company not found or doesn't belong to user
    """
    # Verify company access
    verify_company_access(db, company_id, current_user.id)
    
    db_scenario = HireScenario(
        company_id=company_id,
        role_title=scenario_data.role_title,
        monthly_salary=scenario_data.monthly_salary,
        monthly_benefits=scenario_data.monthly_benefits,
        monthly_overhead=scenario_data.monthly_overhead,
        start_date=scenario_data.start_date
    )
    
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    
    return db_scenario


@router.get("", response_model=List[HireScenarioResponse])
def get_hire_scenarios(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all hire scenarios for a company.
    
    Args:
        company_id: ID of the company
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of hire scenarios
        
    Raises:
        HTTPException: If company not found or doesn't belong to user
    """
    verify_company_access(db, company_id, current_user.id)
    
    scenarios = db.query(HireScenario).filter(
        HireScenario.company_id == company_id
    ).order_by(HireScenario.created_at.desc()).all()
    
    return scenarios


@router.get("/{scenario_id}", response_model=HireScenarioResponse)
def get_hire_scenario(
    scenario_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific hire scenario by ID.
    
    Args:
        scenario_id: Hire scenario ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Hire scenario details
        
    Raises:
        HTTPException: If scenario not found or doesn't belong to user's company
    """
    scenario = db.query(HireScenario).join(Company).filter(
        HireScenario.id == scenario_id,
        Company.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hire scenario not found"
        )
    
    return scenario


@router.patch("/{scenario_id}", response_model=HireScenarioResponse)
def update_hire_scenario(
    scenario_id: int,
    scenario_update: HireScenarioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a hire scenario.
    
    Args:
        scenario_id: Hire scenario ID
        scenario_update: Fields to update
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated hire scenario
        
    Raises:
        HTTPException: If scenario not found or doesn't belong to user's company
    """
    scenario = db.query(HireScenario).join(Company).filter(
        HireScenario.id == scenario_id,
        Company.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hire scenario not found"
        )
    
    # Update only provided fields
    update_data = scenario_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scenario, field, value)
    
    db.commit()
    db.refresh(scenario)
    
    return scenario


@router.delete("/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hire_scenario(
    scenario_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a hire scenario.
    
    Args:
        scenario_id: Hire scenario ID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If scenario not found or doesn't belong to user's company
    """
    scenario = db.query(HireScenario).join(Company).filter(
        HireScenario.id == scenario_id,
        Company.user_id == current_user.id
    ).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hire scenario not found"
        )
    
    db.delete(scenario)
    db.commit()
    
    return None

