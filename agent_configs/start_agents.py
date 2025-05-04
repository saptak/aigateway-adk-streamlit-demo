#!/usr/bin/env python3
"""
Start script for Google ADK agents.
This script initializes and starts all the financial advisor agents.
"""

import os
import sys
import time
import logging
from dotenv import load_dotenv
from google.adk.agents import Agent, LlmAgent
from agent_definitions import (
    create_investment_agent,
    create_loan_agent,
    create_customer_service_agent
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Initialize and start all agents"""
    logger.info("Starting Financial Advisor AI Gateway Demo Agents")
    
    try:
        # Create the agents
        investment_agent = create_investment_agent()
        loan_agent = create_loan_agent()
        customer_service_agent = create_customer_service_agent()
        
        # Create a parent coordinator agent
        coordinator = LlmAgent(
            name="financial_coordinator",
            model="gemini-2.0-pro",
            description="Coordinates financial advisor services by routing queries to specialized agents",
            instruction="""
            You are a Financial Services Coordinator. Your job is to:
            1. Understand user financial questions
            2. Route them to the appropriate specialized agent
            3. Handle general queries directly 
            
            You have these specialized agents:
            - Investment Agent: For stock market, portfolio management, and investment strategy questions
            - Loan Agent: For loan calculations, mortgage queries, and financing options
            - Customer Service Agent: For account issues, general banking questions, and service inquiries
            
            Only route to specialized agents when necessary. Handle simple queries yourself.
            """,
            sub_agents=[
                investment_agent,
                loan_agent,
                customer_service_agent
            ]
        )
        
        logger.info("All agents started successfully")
        
        # Keep the service running
        while True:
            logger.info("Agents running... (Ctrl+C to quit)")
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Shutting down agents")
    except Exception as e:
        logger.error(f"Error starting agents: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
