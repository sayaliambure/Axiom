"""
Financial calculation services for AXIOM.

These services implement the core business logic for:
- Monthly burn rate calculation
- Runway calculation
- Hiring impact analysis
- Risk assessment

All calculations are deterministic and transparent.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple

from .models import FinancialSnapshot, HireScenario, HiringImpact


def calculate_monthly_burn(financial_snapshot: FinancialSnapshot) -> Decimal:
    """
    Calculate monthly burn rate from a financial snapshot.
    
    Formula: Monthly Burn = Monthly Revenue - Monthly Expenses
    
    Assumptions:
        - Negative burn = spending more than earning (typical for early startups)
        - Positive burn = earning more than spending (rare, means company is profitable)
        - Burn rate is assumed constant going forward (no growth/revenue changes)
    
    Args:
        financial_snapshot: The financial snapshot to calculate burn from
        
    Returns:
        Monthly burn rate (negative = cash outflow, positive = cash inflow)
        
    Example:
        If expenses = $50,000/month and revenue = $20,000/month:
        Monthly burn = $20,000 - $50,000 = -$30,000/month (negative burn = losing $30k/month)
    """
    monthly_burn = financial_snapshot.monthly_revenue - financial_snapshot.monthly_expenses
    return monthly_burn


def calculate_runway_months(
    current_cash: Decimal,
    monthly_burn: Decimal
) -> Decimal:
    """
    Calculate runway in months given current cash and monthly burn rate.
    
    Formula: Runway (months) = Current Cash / |Monthly Burn|
    
    Assumptions:
        - Burn rate remains constant (no revenue growth, no expense changes)
        - No additional funding events
        - Company continues operating at current burn rate until cash runs out
        - If monthly burn is positive (profitable), runway is infinite (represented as very large number)
        - If monthly burn is zero, runway is infinite (no cash depletion)
    
    Args:
        current_cash: Current cash balance
        monthly_burn: Monthly burn rate (negative = spending, positive = earning)
        
    Returns:
        Runway in months (rounded to 2 decimal places)
        Returns 999.99 if company is profitable (positive burn or zero burn)
        
    Example:
        Current cash: $300,000
        Monthly burn: -$30,000 (spending $30k more than earning)
        Runway = $300,000 / $30,000 = 10 months
        
    Raises:
        ValueError: If monthly_burn is positive (profitable companies have infinite runway)
    """
    # If company is profitable (positive burn = earning more than spending)
    # or break-even, runway is effectively infinite
    if monthly_burn >= 0:
        # Return a large number to represent "infinite" runway
        # In practice, profitable companies don't need runway calculations
        return Decimal("999.99")
    
    # For negative burn (typical startup case), calculate months until cash runs out
    # Use absolute value since burn is negative
    abs_burn = abs(monthly_burn)
    
    if abs_burn == 0:
        return Decimal("999.99")
    
    runway = current_cash / abs_burn
    
    # Round to 2 decimal places for readability
    return runway.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_burn_after_hire(
    current_monthly_burn: Decimal,
    hire_scenario: HireScenario
) -> Decimal:
    """
    Calculate new monthly burn rate after adding a hire.
    
    Formula: New Burn = Current Burn - Hire Monthly Cost
    
    Note: Since current_burn is typically negative (spending > earning),
    subtracting hire cost makes it more negative (worse burn).
    
    Assumptions:
        - Hire cost is added immediately to monthly expenses
        - No revenue impact from hire (Phase 1 assumption - hire doesn't generate revenue)
        - Hire cost is purely expense, not investment
    
    Args:
        current_monthly_burn: Current monthly burn rate (before hire)
        hire_scenario: The hiring scenario to evaluate
        
    Returns:
        New monthly burn rate after hire
        
    Example:
        Current burn: -$30,000/month
        Hire cost: $12,000/month (salary + benefits + overhead)
        New burn: -$30,000 - $12,000 = -$42,000/month
    """
    hire_monthly_cost = hire_scenario.total_monthly_cost
    # Subtracting hire cost from burn (which is revenue - expenses)
    # Since hire increases expenses, burn becomes more negative
    new_burn = current_monthly_burn - hire_monthly_cost
    return new_burn


def calculate_runway_delta(
    current_runway_months: Decimal,
    new_runway_months: Decimal
) -> Decimal:
    """
    Calculate the change in runway (delta) after a hire.
    
    Formula: Delta = New Runway - Current Runway
    
    Assumptions:
        - Negative delta = runway shortened (typical case)
        - Positive delta = runway extended (only if hire generates revenue > cost, not in Phase 1)
        - Delta is in months
        
    Args:
        current_runway_months: Runway before hire
        new_runway_months: Runway after hire
        
    Returns:
        Change in runway in months (negative = shortened, positive = extended)
        
    Example:
        Current runway: 10 months
        New runway: 7.14 months
        Delta: 7.14 - 10 = -2.86 months (runway shortened by ~3 months)
    """
    delta = new_runway_months - current_runway_months
    return delta.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def assess_risk_level(runway_months: Decimal) -> str:
    """
    Assess hiring risk based on remaining runway.
    
    Risk thresholds:
        - Safe: > 12 months remaining
        - Risky: 6-12 months remaining
        - Dangerous: < 6 months remaining
    
    Assumptions:
        - These thresholds are industry-standard for startup runway planning
        - 12+ months gives buffer for fundraising, pivots, or revenue growth
        - 6-12 months is risky but manageable if fundraising is in progress
        - < 6 months is dangerous - very little room for error
    
    Args:
        runway_months: Remaining runway in months
        
    Returns:
        Risk level: "Safe", "Risky", or "Dangerous"
        
    Example:
        Runway: 8 months → "Risky"
        Runway: 15 months → "Safe"
        Runway: 4 months → "Dangerous"
    """
    # Handle infinite runway (profitable companies)
    if runway_months >= Decimal("999"):
        return "Safe"
    
    if runway_months > Decimal("12"):
        return "Safe"
    elif runway_months >= Decimal("6"):
        return "Risky"
    else:
        return "Dangerous"


def calculate_hiring_impact(
    financial_snapshot: FinancialSnapshot,
    hire_scenario: HireScenario
) -> HiringImpact:
    """
    Calculate the complete hiring impact on runway.
    
    This is the main service function that orchestrates all calculations.
    
    Process:
        1. Calculate current monthly burn
        2. Calculate current runway
        3. Calculate new monthly burn after hire
        4. Calculate new runway after hire
        5. Calculate runway delta
        6. Assess risk level
    
    Assumptions:
        - All calculations assume constant burn rate (no growth)
        - Hire adds to expenses immediately
        - No revenue impact from hire (Phase 1)
        - Company continues at new burn rate until cash runs out
    
    Args:
        financial_snapshot: Current financial state
        hire_scenario: Proposed hiring scenario
        
    Returns:
        HiringImpact object with all calculated metrics
        
    Example:
        Input:
            Financial Snapshot:
                Current cash: $300,000
                Monthly revenue: $20,000
                Monthly expenses: $50,000
            
            Hire Scenario:
                Monthly salary: $10,000
                Monthly benefits: $1,500
                Monthly overhead: $500
        
        Output:
            Current burn: -$30,000/month
            Current runway: 10 months
            New burn: -$42,000/month
            New runway: 7.14 months
            Runway delta: -2.86 months
            Risk: Risky
    """
    # Step 1: Calculate current monthly burn
    current_monthly_burn = calculate_monthly_burn(financial_snapshot)
    
    # Step 2: Calculate current runway
    current_runway_months = calculate_runway_months(
        financial_snapshot.current_cash,
        current_monthly_burn
    )
    
    # Step 3: Calculate new monthly burn after hire
    new_monthly_burn = calculate_burn_after_hire(current_monthly_burn, hire_scenario)
    
    # Step 4: Calculate new runway after hire
    new_runway_months = calculate_runway_months(
        financial_snapshot.current_cash,
        new_monthly_burn
    )
    
    # Step 5: Calculate runway delta
    runway_delta_months = calculate_runway_delta(current_runway_months, new_runway_months)
    
    # Step 6: Assess risk based on new runway
    risk_level = assess_risk_level(new_runway_months)
    
    # Calculate burn delta for completeness
    burn_delta = new_monthly_burn - current_monthly_burn
    
    return HiringImpact(
        current_runway_months=current_runway_months,
        new_runway_months=new_runway_months,
        runway_delta_months=runway_delta_months,
        current_monthly_burn=current_monthly_burn,
        new_monthly_burn=new_monthly_burn,
        burn_delta=burn_delta,
        risk_level=risk_level
    )

