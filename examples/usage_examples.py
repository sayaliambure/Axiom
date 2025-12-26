"""
Usage examples for AXIOM Phase 1: Core Domain & Financial Logic

This file demonstrates how to use the models and services to calculate
hiring impact on runway.
"""

from decimal import Decimal
from datetime import datetime

from src.models import FinancialSnapshot, HireScenario
from src.services import (
    calculate_monthly_burn,
    calculate_runway_months,
    calculate_burn_after_hire,
    calculate_runway_delta,
    assess_risk_level,
    calculate_hiring_impact
)


def example_1_safe_hire():
    """
    Example 1: Safe Hiring Scenario
    
    Company has healthy runway (>12 months) and can afford the hire.
    """
    print("=" * 60)
    print("EXAMPLE 1: Safe Hiring Scenario")
    print("=" * 60)
    
    # Financial snapshot
    snapshot = FinancialSnapshot(
        company_id=1,
        current_cash=Decimal("500000"),  # $500k in the bank
        monthly_revenue=Decimal("30000"),  # $30k MRR
        monthly_expenses=Decimal("45000"),  # $45k monthly expenses
        snapshot_date=datetime.now()
    )
    
    # Proposed hire
    hire = HireScenario(
        company_id=1,
        role_title="Senior Software Engineer",
        monthly_salary=Decimal("12000"),  # $12k/month salary
        monthly_benefits=Decimal("2000"),  # $2k/month benefits
        monthly_overhead=Decimal("500"),  # $500/month overhead
        start_date=datetime.now()
    )
    
    # Calculate impact
    impact = calculate_hiring_impact(snapshot, hire)
    
    print(f"\nFinancial Snapshot:")
    print(f"  Current Cash: ${snapshot.current_cash:,.2f}")
    print(f"  Monthly Revenue: ${snapshot.monthly_revenue:,.2f}")
    print(f"  Monthly Expenses: ${snapshot.monthly_expenses:,.2f}")
    
    print(f"\nProposed Hire:")
    print(f"  Role: {hire.role_title}")
    print(f"  Monthly Cost: ${hire.total_monthly_cost:,.2f}")
    print(f"    - Salary: ${hire.monthly_salary:,.2f}")
    print(f"    - Benefits: ${hire.monthly_benefits:,.2f}")
    print(f"    - Overhead: ${hire.monthly_overhead:,.2f}")
    
    print(f"\nHiring Impact:")
    print(f"  Current Monthly Burn: ${impact.current_monthly_burn:,.2f}")
    print(f"  New Monthly Burn: ${impact.new_monthly_burn:,.2f}")
    print(f"  Burn Increase: ${impact.burn_delta:,.2f}")
    print(f"  Current Runway: {impact.current_runway_months:.2f} months")
    print(f"  New Runway: {impact.new_runway_months:.2f} months")
    print(f"  Runway Delta: {impact.runway_delta_months:.2f} months")
    print(f"  Risk Level: {impact.risk_level}")
    
    print(f"\n💡 Interpretation:")
    print(f"  Hiring this {hire.role_title} will:")
    print(f"  - Increase monthly burn by ${abs(impact.burn_delta):,.2f}")
    print(f"  - Shorten runway by {abs(impact.runway_delta_months):.2f} months")
    print(f"  - Result in {impact.new_runway_months:.2f} months of runway remaining")
    print(f"  - Risk assessment: {impact.risk_level}")
    
    return impact


def example_2_risky_hire():
    """
    Example 2: Risky Hiring Scenario
    
    Company has moderate runway (6-12 months). Hire pushes them into risky territory.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Risky Hiring Scenario")
    print("=" * 60)
    
    # Financial snapshot
    snapshot = FinancialSnapshot(
        company_id=2,
        current_cash=Decimal("240000"),  # $240k in the bank
        monthly_revenue=Decimal("20000"),  # $20k MRR
        monthly_expenses=Decimal("40000"),  # $40k monthly expenses
        snapshot_date=datetime.now()
    )
    
    # Proposed hire
    hire = HireScenario(
        company_id=2,
        role_title="Sales Manager",
        monthly_salary=Decimal("10000"),
        monthly_benefits=Decimal("1800"),
        monthly_overhead=Decimal("700"),
        start_date=datetime.now()
    )
    
    # Calculate impact
    impact = calculate_hiring_impact(snapshot, hire)
    
    print(f"\nFinancial Snapshot:")
    print(f"  Current Cash: ${snapshot.current_cash:,.2f}")
    print(f"  Monthly Revenue: ${snapshot.monthly_revenue:,.2f}")
    print(f"  Monthly Expenses: ${snapshot.monthly_expenses:,.2f}")
    
    print(f"\nProposed Hire:")
    print(f"  Role: {hire.role_title}")
    print(f"  Monthly Cost: ${hire.total_monthly_cost:,.2f}")
    
    print(f"\nHiring Impact:")
    print(f"  Current Runway: {impact.current_runway_months:.2f} months")
    print(f"  New Runway: {impact.new_runway_months:.2f} months")
    print(f"  Runway Delta: {impact.runway_delta_months:.2f} months")
    print(f"  Risk Level: {impact.risk_level}")
    
    print(f"\n⚠️  Interpretation:")
    print(f"  This hire reduces runway to {impact.new_runway_months:.2f} months.")
    print(f"  Risk level: {impact.risk_level} - Consider fundraising timeline.")
    
    return impact


def example_3_dangerous_hire():
    """
    Example 3: Dangerous Hiring Scenario
    
    Company has limited runway. Hire pushes them into dangerous territory (<6 months).
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Dangerous Hiring Scenario")
    print("=" * 60)
    
    # Financial snapshot
    snapshot = FinancialSnapshot(
        company_id=3,
        current_cash=Decimal("150000"),  # $150k in the bank
        monthly_revenue=Decimal("15000"),  # $15k MRR
        monthly_expenses=Decimal("35000"),  # $35k monthly expenses
        snapshot_date=datetime.now()
    )
    
    # Proposed hire
    hire = HireScenario(
        company_id=3,
        role_title="VP of Engineering",
        monthly_salary=Decimal("15000"),  # Higher salary role
        monthly_benefits=Decimal("2500"),
        monthly_overhead=Decimal("1000"),
        start_date=datetime.now()
    )
    
    # Calculate impact
    impact = calculate_hiring_impact(snapshot, hire)
    
    print(f"\nFinancial Snapshot:")
    print(f"  Current Cash: ${snapshot.current_cash:,.2f}")
    print(f"  Monthly Revenue: ${snapshot.monthly_revenue:,.2f}")
    print(f"  Monthly Expenses: ${snapshot.monthly_expenses:,.2f}")
    
    print(f"\nProposed Hire:")
    print(f"  Role: {hire.role_title}")
    print(f"  Monthly Cost: ${hire.total_monthly_cost:,.2f}")
    
    print(f"\nHiring Impact:")
    print(f"  Current Runway: {impact.current_runway_months:.2f} months")
    print(f"  New Runway: {impact.new_runway_months:.2f} months")
    print(f"  Runway Delta: {impact.runway_delta_months:.2f} months")
    print(f"  Risk Level: {impact.risk_level}")
    
    print(f"\n🚨 Interpretation:")
    print(f"  This hire reduces runway to {impact.new_runway_months:.2f} months.")
    print(f"  Risk level: {impact.risk_level} - HIGH RISK!")
    print(f"  Recommendation: Delay hire or secure funding first.")
    
    return impact


def example_4_step_by_step_calculations():
    """
    Example 4: Step-by-step calculation breakdown
    
    Shows how each service function works individually.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Step-by-Step Calculation Breakdown")
    print("=" * 60)
    
    snapshot = FinancialSnapshot(
        company_id=4,
        current_cash=Decimal("360000"),
        monthly_revenue=Decimal("25000"),
        monthly_expenses=Decimal("50000"),
        snapshot_date=datetime.now()
    )
    
    hire = HireScenario(
        company_id=4,
        role_title="Product Manager",
        monthly_salary=Decimal("11000"),
        monthly_benefits=Decimal("1900"),
        monthly_overhead=Decimal("600"),
        start_date=datetime.now()
    )
    
    print(f"\nStep 1: Calculate Monthly Burn")
    current_burn = calculate_monthly_burn(snapshot)
    print(f"  Monthly Burn = Revenue - Expenses")
    print(f"  Monthly Burn = ${snapshot.monthly_revenue:,.2f} - ${snapshot.monthly_expenses:,.2f}")
    print(f"  Monthly Burn = ${current_burn:,.2f}")
    
    print(f"\nStep 2: Calculate Current Runway")
    current_runway = calculate_runway_months(snapshot.current_cash, current_burn)
    print(f"  Runway = Current Cash / |Monthly Burn|")
    print(f"  Runway = ${snapshot.current_cash:,.2f} / ${abs(current_burn):,.2f}")
    print(f"  Runway = {current_runway:.2f} months")
    
    print(f"\nStep 3: Calculate Burn After Hire")
    new_burn = calculate_burn_after_hire(current_burn, hire)
    print(f"  New Burn = Current Burn - Hire Cost")
    print(f"  New Burn = ${current_burn:,.2f} - ${hire.total_monthly_cost:,.2f}")
    print(f"  New Burn = ${new_burn:,.2f}")
    
    print(f"\nStep 4: Calculate New Runway")
    new_runway = calculate_runway_months(snapshot.current_cash, new_burn)
    print(f"  New Runway = ${snapshot.current_cash:,.2f} / ${abs(new_burn):,.2f}")
    print(f"  New Runway = {new_runway:.2f} months")
    
    print(f"\nStep 5: Calculate Runway Delta")
    delta = calculate_runway_delta(current_runway, new_runway)
    print(f"  Delta = New Runway - Current Runway")
    print(f"  Delta = {new_runway:.2f} - {current_runway:.2f}")
    print(f"  Delta = {delta:.2f} months")
    
    print(f"\nStep 6: Assess Risk Level")
    risk = assess_risk_level(new_runway)
    print(f"  New Runway: {new_runway:.2f} months")
    print(f"  Risk Level: {risk}")
    print(f"  (Safe: >12mo, Risky: 6-12mo, Dangerous: <6mo)")


if __name__ == "__main__":
    # Run all examples
    example_1_safe_hire()
    example_2_risky_hire()
    example_3_dangerous_hire()
    example_4_step_by_step_calculations()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)

