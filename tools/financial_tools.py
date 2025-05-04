"""
Financial calculation tools for use with ADK agents.
These tools provide specialized financial functions for the agents.
"""

import numpy as np
import numpy_financial as npf
import requests
import os
from typing import Dict, List, Union, Optional
from datetime import datetime, timedelta
import json

# Mock API for stock data (in a real app, you'd use a real financial API)
STOCK_API_BASE_URL = os.getenv("STOCK_API_URL", "https://api.example.com/stocks")
FX_API_BASE_URL = os.getenv("FX_API_URL", "https://api.example.com/fx")
API_KEY = os.getenv("FINANCIAL_API_KEY", "demo-key")

def calculate_loan_payment(
    principal: float,
    annual_interest_rate: float,
    loan_term_years: int,
    payment_frequency: str = "monthly"
) -> Dict[str, Union[float, List[Dict[str, float]]]]:
    """
    Calculate loan payment details including monthly payment and amortization schedule.
    
    Args:
        principal: Loan amount in currency units
        annual_interest_rate: Annual interest rate as a percentage (e.g., 5.5 for 5.5%)
        loan_term_years: Length of the loan in years
        payment_frequency: Frequency of payments ('monthly', 'biweekly', 'weekly')
        
    Returns:
        Dict containing payment amount and amortization schedule
    """
    # Convert annual rate to decimal
    rate = annual_interest_rate / 100
    
    # Adjust rate and periods based on payment frequency
    if payment_frequency == "monthly":
        periods = loan_term_years * 12
        periodic_rate = rate / 12
    elif payment_frequency == "biweekly":
        periods = loan_term_years * 26
        periodic_rate = rate / 26
    elif payment_frequency == "weekly":
        periods = loan_term_years * 52
        periodic_rate = rate / 52
    else:
        raise ValueError("Payment frequency must be 'monthly', 'biweekly', or 'weekly'")
    
    # Calculate payment amount
    payment = -npf.pmt(periodic_rate, periods, principal)
    
    # Generate abbreviated amortization schedule (first 3 payments)
    schedule = []
    balance = principal
    
    for period in range(1, min(4, periods + 1)):
        interest_payment = balance * periodic_rate
        principal_payment = payment - interest_payment
        balance -= principal_payment
        
        schedule.append({
            "period": period,
            "payment": round(payment, 2),
            "principal": round(principal_payment, 2),
            "interest": round(interest_payment, 2),
            "balance": round(balance, 2)
        })
    
    return {
        "payment_amount": round(payment, 2),
        "payment_frequency": payment_frequency,
        "total_payments": periods,
        "total_interest": round((payment * periods) - principal, 2),
        "amortization_preview": schedule
    }

def calculate_mortgage_payment(
    home_price: float,
    down_payment: float,
    annual_interest_rate: float,
    loan_term_years: int,
    property_tax_rate: float = 1.0,
    annual_insurance: float = 1000,
    include_pmi: bool = True
) -> Dict[str, float]:
    """
    Calculate detailed mortgage payment information.
    
    Args:
        home_price: Price of the home in currency units
        down_payment: Down payment amount in currency units
        annual_interest_rate: Annual interest rate as a percentage
        loan_term_years: Length of the mortgage in years
        property_tax_rate: Annual property tax rate as a percentage
        annual_insurance: Annual home insurance cost
        include_pmi: Whether to include Private Mortgage Insurance (if down payment < 20%)
        
    Returns:
        Dict containing payment details
    """
    # Calculate loan amount
    loan_amount = home_price - down_payment
    down_payment_percent = (down_payment / home_price) * 100
    
    # Calculate base monthly payment (principal + interest)
    monthly_rate = annual_interest_rate / 100 / 12
    num_payments = loan_term_years * 12
    monthly_pi = -npf.pmt(monthly_rate, num_payments, loan_amount)
    
    # Calculate taxes and insurance
    monthly_property_tax = (home_price * property_tax_rate / 100) / 12
    monthly_insurance = annual_insurance / 12
    
    # Calculate PMI if applicable (typically 0.5-1% annually if down payment < 20%)
    monthly_pmi = 0
    if include_pmi and down_payment_percent < 20:
        pmi_rate = 0.5 + ((20 - down_payment_percent) * 0.025)  # Higher PMI for lower down payments
        monthly_pmi = (loan_amount * pmi_rate / 100) / 12
    
    # Calculate total payment
    total_monthly_payment = monthly_pi + monthly_property_tax + monthly_insurance + monthly_pmi
    
    return {
        "loan_amount": round(loan_amount, 2),
        "down_payment_percent": round(down_payment_percent, 2),
        "monthly_principal_interest": round(monthly_pi, 2),
        "monthly_property_tax": round(monthly_property_tax, 2),
        "monthly_insurance": round(monthly_insurance, 2),
        "monthly_pmi": round(monthly_pmi, 2),
        "total_monthly_payment": round(total_monthly_payment, 2),
        "total_payment_over_term": round(total_monthly_payment * num_payments, 2)
    }

def calculate_investment_returns(
    initial_investment: float,
    monthly_contribution: float,
    annual_return_rate: float,
    investment_period_years: int,
    compound_frequency: str = "monthly",
    tax_rate: Optional[float] = None
) -> Dict[str, Union[float, List[Dict[str, float]]]]:
    """
    Calculate investment returns with regular contributions over time.
    
    Args:
        initial_investment: Starting investment amount
        monthly_contribution: Regular monthly contributions
        annual_return_rate: Expected annual return rate as a percentage
        investment_period_years: Investment time horizon in years
        compound_frequency: How often returns compound ('monthly', 'quarterly', 'annually')
        tax_rate: Optional tax rate as a percentage (for after-tax calculations)
        
    Returns:
        Dict containing investment growth details
    """
    # Convert annual rate to decimal
    rate = annual_return_rate / 100
    
    # Set compounding periods based on frequency
    if compound_frequency == "monthly":
        periods_per_year = 12
    elif compound_frequency == "quarterly":
        periods_per_year = 4
    elif compound_frequency == "annually":
        periods_per_year = 1
    else:
        raise ValueError("Compound frequency must be 'monthly', 'quarterly', or 'annually'")
    
    # Calculate periodic rate and total periods
    periodic_rate = rate / periods_per_year
    total_periods = investment_period_years * periods_per_year
    
    # Calculate contribution per period
    period_contribution = monthly_contribution * (12 / periods_per_year)
    
    # Calculate final value with regular contributions
    future_value = initial_investment * (1 + periodic_rate) ** total_periods
    
    # Calculate future value of periodic contributions
    # Future value of an annuity formula
    if periodic_rate > 0:
        contribution_future_value = period_contribution * ((1 + periodic_rate) ** total_periods - 1) / periodic_rate
    else:
        contribution_future_value = period_contribution * total_periods
    
    total_future_value = future_value + contribution_future_value
    total_contributions = initial_investment + (monthly_contribution * 12 * investment_period_years)
    total_earnings = total_future_value - total_contributions
    
    # Calculate after-tax values if tax rate is provided
    after_tax_earnings = total_earnings
    after_tax_future_value = total_future_value
    
    if tax_rate is not None:
        tax_rate_decimal = tax_rate / 100
        after_tax_earnings = total_earnings * (1 - tax_rate_decimal)
        after_tax_future_value = total_contributions + after_tax_earnings
    
    # Generate year-by-year growth summary (for first 5 years)
    yearly_summary = []
    current_value = initial_investment
    
    for year in range(1, min(6, investment_period_years + 1)):
        year_start_value = current_value
        
        # Compound through the year
        for _ in range(periods_per_year):
            current_value = current_value * (1 + periodic_rate) + period_contribution
        
        yearly_contribution = monthly_contribution * 12
        yearly_growth = current_value - year_start_value - yearly_contribution
        
        yearly_summary.append({
            "year": year,
            "start_value": round(year_start_value, 2),
            "contributions": round(yearly_contribution, 2),
            "growth": round(yearly_growth, 2),
            "end_value": round(current_value, 2)
        })
    
    return {
        "total_future_value": round(total_future_value, 2),
        "total_contributions": round(total_contributions, 2),
        "total_earnings": round(total_earnings, 2),
        "after_tax_earnings": round(after_tax_earnings, 2) if tax_rate is not None else None,
        "after_tax_future_value": round(after_tax_future_value, 2) if tax_rate is not None else None,
        "compound_frequency": compound_frequency,
        "yearly_summary": yearly_summary
    }

def fetch_stock_price(
    ticker_symbol: str,
    data_points: int = 1
) -> Dict[str, Union[float, List[Dict[str, float]]]]:
    """
    Fetch stock price data for a given ticker symbol.
    
    Args:
        ticker_symbol: Stock ticker symbol (e.g., 'AAPL' for Apple)
        data_points: Number of historical data points to retrieve (1 = latest only)
        
    Returns:
        Dict containing stock price information
    """
    # In a real implementation, this would call a financial data API
    # For this demo, we'll generate mock data
    
    # Mock API call for demo purposes
    try:
        # Simulate API request
        print(f"Fetching stock data for {ticker_symbol}")
        
        # Generate mock data based on ticker
        base_price = sum(ord(c) for c in ticker_symbol) % 300 + 50  # Generate a price between $50-$350
        
        # Create mock response
        mock_data = {
            "ticker": ticker_symbol.upper(),
            "company_name": f"{ticker_symbol.title()} Inc.",
            "current_price": round(base_price, 2),
            "currency": "USD",
            "change_percent": round((np.random.random() * 6) - 3, 2),  # -3% to +3%
            "market_cap": round(base_price * (10 ** 9) / 100, 2),
            "timestamp": datetime.now().isoformat(),
            "historical_data": []
        }
        
        # Add historical data points if requested
        if data_points > 1:
            for i in range(1, data_points):
                days_ago = i
                price_modifier = 1 + ((np.random.random() * 0.1) - 0.05)  # -5% to +5% daily change
                historical_price = round(base_price * price_modifier, 2)
                
                mock_data["historical_data"].append({
                    "date": (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d"),
                    "price": historical_price,
                    "volume": int(np.random.random() * 10000000) + 1000000
                })
        
        return mock_data
        
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to fetch stock data: {str(e)}"
        }

def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    amount: float = 1.0
) -> Dict[str, Union[float, str]]:
    """
    Get current exchange rate between two currencies.
    
    Args:
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
        amount: Amount to convert
        
    Returns:
        Dict containing exchange rate information
    """
    # In a real implementation, this would call a currency exchange API
    # For this demo, we'll generate mock data
    
    # Mock exchange rates against USD
    mock_rates = {
        'USD': 1.0,
        'EUR': 0.93,
        'GBP': 0.78,
        'JPY': 151.2,
        'CAD': 1.37,
        'AUD': 1.52,
        'CHF': 0.91,
        'CNY': 7.25,
        'INR': 83.4,
        'MXN': 16.8
    }
    
    # Normalize currency codes
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    try:
        # Check if currencies are supported
        if from_currency not in mock_rates or to_currency not in mock_rates:
            return {
                "error": True,
                "message": f"Currency not supported. Supported currencies: {', '.join(mock_rates.keys())}"
            }
        
        # Calculate exchange rate
        usd_to_from = mock_rates[from_currency]
        usd_to_to = mock_rates[to_currency]
        
        # Calculate rate from from_currency to to_currency
        rate = usd_to_to / usd_to_from
        converted_amount = amount * rate
        
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": round(rate, 6),
            "amount": amount,
            "converted_amount": round(converted_amount, 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": True,
            "message": f"Failed to get exchange rate: {str(e)}"
        }
