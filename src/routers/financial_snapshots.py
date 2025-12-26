"""
Financial snapshot CRUD routes.

All operations are scoped to the user's companies.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..db_models import User, Company, FinancialSnapshot
from ..schemas import (
    FinancialSnapshotCreate,
    FinancialSnapshotUpdate,
    FinancialSnapshotResponse
)
from ..auth import get_current_user

router = APIRouter(prefix="/financial-snapshots", tags=["financial-snapshots"])


def verify_company_access(db: Session, company_id: int, user_id: int) -> Company:
    """
    Verify that a company belongs to the user.
    
    Args:
        db: Database session
        company_id: Company ID to verify
        user_id: User ID to check ownership
        
    Returns:
        Company object if access is granted
        
    Raises:
        HTTPException: If company not found or doesn't belong to user
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == user_id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company


@router.post("", response_model=FinancialSnapshotResponse, status_code=status.HTTP_201_CREATED)
def create_financial_snapshot(
    snapshot_data: FinancialSnapshotCreate,
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new financial snapshot for a company.
    
    Args:
        snapshot_data: Financial snapshot data
        company_id: ID of the company
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created financial snapshot
        
    Raises:
        HTTPException: If company not found or doesn't belong to user
    """
    # Verify company access
    verify_company_access(db, company_id, current_user.id)
    
    db_snapshot = FinancialSnapshot(
        company_id=company_id,
        current_cash=snapshot_data.current_cash,
        monthly_revenue=snapshot_data.monthly_revenue,
        monthly_expenses=snapshot_data.monthly_expenses,
        snapshot_date=snapshot_data.snapshot_date
    )
    
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    
    return db_snapshot


@router.get("", response_model=List[FinancialSnapshotResponse])
def get_financial_snapshots(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all financial snapshots for a company.
    
    Args:
        company_id: ID of the company
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of financial snapshots
        
    Raises:
        HTTPException: If company not found or doesn't belong to user
    """
    verify_company_access(db, company_id, current_user.id)
    
    snapshots = db.query(FinancialSnapshot).filter(
        FinancialSnapshot.company_id == company_id
    ).order_by(FinancialSnapshot.created_at.desc()).all()
    
    return snapshots


@router.get("/{snapshot_id}", response_model=FinancialSnapshotResponse)
def get_financial_snapshot(
    snapshot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific financial snapshot by ID.
    
    Args:
        snapshot_id: Financial snapshot ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Financial snapshot details
        
    Raises:
        HTTPException: If snapshot not found or doesn't belong to user's company
    """
    snapshot = db.query(FinancialSnapshot).join(Company).filter(
        FinancialSnapshot.id == snapshot_id,
        Company.user_id == current_user.id
    ).first()
    
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial snapshot not found"
        )
    
    return snapshot


@router.patch("/{snapshot_id}", response_model=FinancialSnapshotResponse)
def update_financial_snapshot(
    snapshot_id: int,
    snapshot_update: FinancialSnapshotUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a financial snapshot.
    
    Args:
        snapshot_id: Financial snapshot ID
        snapshot_update: Fields to update
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated financial snapshot
        
    Raises:
        HTTPException: If snapshot not found or doesn't belong to user's company
    """
    snapshot = db.query(FinancialSnapshot).join(Company).filter(
        FinancialSnapshot.id == snapshot_id,
        Company.user_id == current_user.id
    ).first()
    
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial snapshot not found"
        )
    
    # Update only provided fields
    update_data = snapshot_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(snapshot, field, value)
    
    db.commit()
    db.refresh(snapshot)
    
    return snapshot


@router.delete("/{snapshot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_financial_snapshot(
    snapshot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a financial snapshot.
    
    Args:
        snapshot_id: Financial snapshot ID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If snapshot not found or doesn't belong to user's company
    """
    snapshot = db.query(FinancialSnapshot).join(Company).filter(
        FinancialSnapshot.id == snapshot_id,
        Company.user_id == current_user.id
    ).first()
    
    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial snapshot not found"
        )
    
    db.delete(snapshot)
    db.commit()
    
    return None

