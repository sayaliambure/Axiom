"""
Company routes.

Note: In MVP, we assume one company per user for simplicity.
Future versions could support multiple companies per user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..db_models import User, Company
from ..schemas import CompanyCreate, CompanyResponse
from ..auth import get_current_user

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new company for the current user.
    
    Args:
        company_data: Company creation data (name)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created company
    """
    db_company = Company(
        name=company_data.name,
        user_id=current_user.id
    )
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company


@router.get("", response_model=list[CompanyResponse])
def get_companies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all companies for the current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of user's companies
    """
    companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific company by ID.
    
    Args:
        company_id: Company ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Company details
        
    Raises:
        HTTPException: If company not found or doesn't belong to user
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company

