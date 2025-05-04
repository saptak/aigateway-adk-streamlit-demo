"""
Agent definitions for the Financial Advisor AI Gateway Demo.
This module contains the specialized agents for different financial services.
"""

from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from tools.financial_tools import (
    calculate_loan_payment,
    calculate_investment_returns,
    fetch_stock_price,
    calculate_mortgage_payment,
    get_exchange_rate
)

def create_investment_agent():
    """
    Creates an agent specialized in investment advice.
    
    Returns:
        Agent: The configured investment advisor agent
    """
    return LlmAgent(
        name="investment_advisor",
        model="gemini-2.0-pro",
        description="Provides investment advice and portfolio management guidance",
        instruction="""
        You are a Financial Investment Advisor. Your responsibilities include:
        
        1. Providing investment advice based on user goals and risk tolerance
        2. Analyzing portfolio allocations and suggesting optimizations
        3. Explaining investment concepts and market trends
        4. Using financial tools to calculate investment returns
        5. Providing factual information about stocks and market data
        
        Be professional, thorough, and consider long-term investment horizons.
        Always clarify that you're providing educational information, not financial advice.
        """,
        tools=[
            calculate_investment_returns,
            fetch_stock_price,
            google_search
        ]
    )

def create_loan_agent():
    """
    Creates an agent specialized in loan calculations and financing.
    
    Returns:
        Agent: The configured loan specialist agent
    """
    return LlmAgent(
        name="loan_specialist",
        model="gemini-2.0-pro",
        description="Provides loan calculations and financing information",
        instruction="""
        You are a Loan Specialist. Your responsibilities include:
        
        1. Calculating loan payments and amortization schedules
        2. Explaining different financing options and their pros/cons
        3. Providing mortgage information and calculations
        4. Explaining loan concepts (interest rates, APR, fees)
        5. Helping compare different loan options
        
        Be concise, accurate, and educational in your responses.
        Always clarify that you're providing educational information, not financial advice.
        """,
        tools=[
            calculate_loan_payment,
            calculate_mortgage_payment,
            get_exchange_rate
        ]
    )

def create_customer_service_agent():
    """
    Creates an agent specialized in customer service for banking.
    
    Returns:
        Agent: The configured customer service agent
    """
    return LlmAgent(
        name="customer_service",
        model="gemini-2.0-pro",
        description="Assists with general banking questions and customer service",
        instruction="""
        You are a Financial Customer Service Representative. Your responsibilities include:
        
        1. Answering general banking questions
        2. Explaining account features and services
        3. Providing guidance on typical banking procedures
        4. Directing users to appropriate resources
        5. Offering friendly, patient assistance
        
        Be empathetic, clear, and helpful. Use simple language and avoid jargon.
        Never request or provide access to real accounts.
        """,
        tools=[
            google_search
        ]
    )
