"""
Mock Envoy AI Gateway API for development and testing.
"""

import random
import time
import json
from typing import Dict, Any, List, Union
import numpy as np
from datetime import datetime

# Sample responses for different query types
INVESTMENT_RESPONSES = [
    "Based on your risk tolerance and goals, I recommend a diversified portfolio with 60% stocks, 30% bonds, and 10% cash equivalents. This allocation provides a good balance between growth and stability.",
    "For long-term investment, index funds are generally a cost-effective strategy. Consider allocating a portion of your portfolio to a total market index fund to gain broad market exposure.",
    "Dollar-cost averaging can be an effective strategy for investing in volatile markets. By investing a fixed amount regularly, you buy more shares when prices are low and fewer when prices are high.",
    "When planning for retirement, consider tax-advantaged accounts like 401(k)s and IRAs. These accounts offer tax benefits that can significantly increase your long-term returns."
]

LOAN_RESPONSES = [
    "Based on your income and debt-to-income ratio, you might qualify for a mortgage of approximately $350,000. With current interest rates, your monthly payment would be around $1,800 including principal, interest, taxes, and insurance.",
    "For a $25,000 auto loan over 5 years at 4.5% interest, your monthly payment would be approximately $466. The total interest paid over the life of the loan would be about $2,960.",
    "Refinancing your mortgage could make sense if you can lower your interest rate by at least 0.75 percentage points. With current rates, you could save approximately $200 per month on your payment.",
    "When comparing loan offers, pay attention to the APR, not just the interest rate. The APR includes fees and gives you a more accurate picture of the total cost of borrowing."
]

CUSTOMER_SERVICE_RESPONSES = [
    "To open a new account, you'll need to provide identification (such as a driver's license or passport), proof of address, and your Social Security number. You can start this process online or visit a branch for assistance.",
    "Mobile check deposit is available through our mobile app. Simply endorse the check, take photos of the front and back, and submit through the app. Funds are typically available within 1-2 business days.",
    "Our international wire transfer service allows you to send money worldwide. Transfers typically arrive within 1-3 business days, and fees vary based on the destination country and amount sent.",
    "If you notice an unauthorized transaction on your account, please contact us immediately at our fraud hotline. Your liability is limited if you report fraud promptly."
]

GENERAL_RESPONSES = [
    "Financial planning is a process that helps you make informed decisions about your money to achieve your life goals. It typically includes budgeting, saving, investing, debt management, and insurance planning.",
    "A good emergency fund typically contains 3-6 months of essential expenses, kept in easily accessible accounts like high-yield savings accounts or money market funds.",
    "The Rule of 72 is a simple way to estimate how long it will take for an investment to double. Divide 72 by the annual return rate to get the approximate number of years.",
    "Compound interest is the addition of interest to the principal sum of a loan or deposit, or in other words, interest on interest. It is the result of reinvesting interest, rather than paying it out."
]

# Model information
MODELS = {
    "investment": [
        {"name": "gpt-4-1106-preview", "provider": "openai", "latency_range": (0.8, 1.5)},
        {"name": "claude-3-opus-20240229", "provider": "anthropic", "latency_range": (0.9, 1.7)}
    ],
    "investment-local": [
        {"name": "llama3-8b", "provider": "ollama", "latency_range": (0.3, 0.8)},
        {"name": "mistral-7b", "provider": "ollama", "latency_range": (0.2, 0.7)}
    ],
    "loan": [
        {"name": "gpt-4-1106-preview", "provider": "openai", "latency_range": (0.5, 1.2)}
    ],
    "loan-local": [
        {"name": "llama3-8b", "provider": "ollama", "latency_range": (0.2, 0.6)},
        {"name": "phi-2", "provider": "ollama", "latency_range": (0.1, 0.5)}
    ],
    "customer": [
        {"name": "claude-3-sonnet-20240229", "provider": "anthropic", "latency_range": (0.7, 1.3)}
    ],
    "customer-local": [
        {"name": "mistral-7b", "provider": "ollama", "latency_range": (0.2, 0.7)},
        {"name": "solar-10.7b", "provider": "ollama", "latency_range": (0.3, 0.9)}
    ],
    "general": [
        {"name": "gemini-1.5-pro", "provider": "google", "latency_range": (0.6, 1.1)}
    ]
}

# Ollama models
OLLAMA_MODELS = ["llama3-8b", "mistral-7b", "phi-2", "codellama-7b", "solar-10.7b"]

def simulate_token_count(text: str) -> int:
    """Estimate token count from text"""
    # Rough approximation: 1 token ≈ 4 characters
    return len(text) // 4

def get_mock_response(route: str, prompt: str, demo_modes: List[str], custom_model: str = None) -> Dict[str, Any]:
    """
    Generate a mock response as if it came from the Envoy AI Gateway.
    
    Args:
        route: API route (/v1/investment, /v1/loan, etc.)
        prompt: User's prompt text
        demo_modes: Enabled demo features
        custom_model: Optional specific model to use (for Ollama)
        
    Returns:
        Dict containing the mocked API response
    """
    # Determine query type from route
    query_type = route.split("/")[-1]
    
    # Select appropriate response set
    if "investment" in query_type:
        responses = INVESTMENT_RESPONSES
        model_category = "investment-local" if "local" in query_type else "investment"
        model_info = random.choice(MODELS[model_category])
    elif "loan" in query_type:
        responses = LOAN_RESPONSES
        model_category = "loan-local" if "local" in query_type else "loan"
        model_info = random.choice(MODELS[model_category])
    elif "customer" in query_type:
        responses = CUSTOMER_SERVICE_RESPONSES
        model_category = "customer-local" if "local" in query_type else "customer"
        model_info = random.choice(MODELS[model_category])
    else:
        responses = GENERAL_RESPONSES
        model_info = random.choice(MODELS["general"])
    
    # Override model if custom model specified (for Ollama)
    if custom_model and custom_model in OLLAMA_MODELS:
        model_info = {
            "name": custom_model,
            "provider": "ollama",
            "latency_range": (0.2, 0.8)  # Generic latency range for local models
        }
    
    # Select a response
    response_text = random.choice(responses)
    
    # Simulate latency if enabled
    if "Latency Metrics" in demo_modes:
        min_latency, max_latency = model_info["latency_range"]
        simulated_latency = random.uniform(min_latency, max_latency)
        time.sleep(simulated_latency)
    
    # Simulate token usage
    input_tokens = simulate_token_count(prompt)
    output_tokens = simulate_token_count(response_text)
    
    # Simulate rate limiting if enabled
    rate_limited = False
    if "Rate Limiting" in demo_modes:
        # 10% chance of rate limiting for cloud models, 3% for local models
        rate_limit_chance = 0.03 if model_info["provider"] == "ollama" else 0.1
        rate_limited = random.random() < rate_limit_chance
    
    if rate_limited:
        return {
            "error": "rate_limit_exceeded",
            "message": "You have exceeded your rate limit. Please try again later.",
            "retry_after": 30
        }
    
    # Simulate model fallback if enabled
    used_fallback = False
    original_model = model_info["name"]
    if "Model Fallback" in demo_modes:
        # 15% chance of fallback for cloud models, 5% for local models
        fallback_chance = 0.05 if model_info["provider"] == "ollama" else 0.15
        used_fallback = random.random() < fallback_chance
        if used_fallback:
            # Select a different model as fallback
            model_key = model_category if model_category in MODELS else query_type
            fallback_options = [m for m in MODELS[model_key] if m["name"] != original_model]
            if fallback_options:
                model_info = random.choice(fallback_options)
    
    # Build the response
    return {
        "response": response_text,
        "model": model_info["name"],
        "provider": model_info["provider"],
        "used_fallback": used_fallback,
        "original_model": original_model if used_fallback else None,
        "timestamp": datetime.now().isoformat(),
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens
        },
        "request_id": f"req_{random.randint(10000, 99999)}"
    }
