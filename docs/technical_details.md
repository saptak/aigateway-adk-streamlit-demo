# Technical Implementation Details

This document provides a detailed explanation of how the Financial Advisor AI Gateway Demo is implemented.

## Architecture Overview

The application follows a layered architecture:

```
┌───────────────┐
│  Streamlit UI │
└───────┬───────┘
        │
┌───────▼───────┐
│  Envoy AI     │
│  Gateway      │
└───────┬───────┘
        │
┌───────▼───────┐
│  Google ADK   │
│  Agents       │
└───────┬───────┘
        │
┌───────▼───────┐
│  LLM Providers│
│  (OpenAI,     │
│  Anthropic,   │
│  Google)      │
└───────────────┘
```

### Key Components

1. **Streamlit UI**: User interface for the financial chatbot
2. **Envoy AI Gateway**: Manages traffic between the UI and LLMs
3. **Google ADK Agents**: Specialized agents for different financial tasks
4. **LLM Providers**: Multiple model providers for different query types

## Envoy AI Gateway Implementation

### Configuration Structure

The Envoy AI Gateway configuration (`envoy_config.yaml`) defines how requests are routed, rate limited, and secured.

#### Listener Configuration

```yaml
listeners:
  - name: main
    port: 9000
    protocol: http
```

This defines the main entry point for the gateway, exposing an HTTP API on port 9000.

#### Rate Limiting

```yaml
rateLimits:
  - name: token-based-limit
    tokenLimits:
      - provider: openai
        inputTokensPerSecond: 5000
        outputTokensPerSecond: 2500
```

This implements token-based rate limiting per provider, which is more appropriate for LLM traffic than request-based limits. This allows fine-grained control over usage and costs.

#### Route Configuration

```yaml
routes:
  - name: investment-advisor
    matches:
      - path: /v1/investment
    backends:
      - name: openai-investment-backend
        priority: 1
        provider:
          openai:
            model: gpt-4-1106-preview
            temperature: 0.3
            maxOutputTokens: 1024
      - name: anthropic-investment-backend
        priority: 2
        provider:
          anthropic:
            model: claude-3-opus-20240229
            temperature: 0.3
            maxOutputTokens: 1024
```

Each route defines:
- A URL path pattern to match requests
- Multiple backends with priority ordering (for fallback)
- Provider-specific configuration (model, parameters, etc.)

#### Security Policies

```yaml
securityPolicy:
  authentication:
    jwtProvider:
      issuer: "fintech-demo-issuer"
      audiences: ["financial-advisor-app"]
      remoteJwks:
        uri: "https://example.com/.well-known/jwks.json"
        httpTimeout: 5s
        cacheDuration: 300s
```

Security policies define authentication requirements for each route. In this case, we're using JWT authentication with a remote JWKS endpoint.

#### Observability Configuration

```yaml
observability:
  logging:
    level: info
    format: json
    destination:
      stdout: {}
  metrics:
    prometheus:
      scrape: true
      path: /metrics
      port: 9901
```

This configures logging and metrics collection for the gateway, enabling detailed observability.

## Google ADK Agent Implementation

### Agent Structure

The agent implementation uses Google's Agent Development Kit to create a hierarchy of specialized agents:

```
                 ┌───────────────────┐
                 │ Coordinator Agent │
                 └─────────┬─────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
┌──────────▼─────────┐ ┌───▼───────────┐ ┌─▼──────────────┐
│ Investment Advisor │ │ Loan Specialist│ │ Customer Service│
└────────────────────┘ └───────────────┘ └────────────────┘
```

### Agent Definitions

Each agent (`agent_definitions.py`) is configured with:

1. **Name and Description**: For identification and routing
2. **Model Configuration**: Specifies which LLM to use
3. **Instructions**: Custom system prompt for the agent's role
4. **Tools**: Special functions the agent can use

For example, the Investment Advisor agent:

```python
def create_investment_agent():
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
```

### Coordinator Logic

The coordinator agent (`start_agents.py`) manages routing between specialized agents:

```python
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
```

The coordinator uses the agent descriptions to determine which specialized agent is best suited for each query.

## Financial Tools Implementation

The demo includes several specialized financial tools (`financial_tools.py`):

1. **calculate_loan_payment**: Calculates loan details including amortization schedules
2. **calculate_mortgage_payment**: Provides detailed mortgage payment breakdowns
3. **calculate_investment_returns**: Projects investment growth with contributions
4. **fetch_stock_price**: Retrieves stock price information (mock data for demo)
5. **get_exchange_rate**: Gets currency exchange rates (mock data for demo)

These tools enable the agents to perform specific financial calculations and provide accurate numeric responses.

## Streamlit UI Implementation

The Streamlit UI (`app.py`) provides a user-friendly interface with:

1. **Chat Interface**: For user queries and AI responses
2. **Configuration Options**: To demonstrate different features
3. **Metrics Visualization**: To display usage, latency, and routing data

### Key UI Components

#### Session State Management

```python
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "token_usage" not in st.session_state:
    st.session_state.token_usage = {"input": 0, "output": 0}

if "request_history" not in st.session_state:
    # Store timestamp, request_type, model, latency, tokens
    st.session_state.request_history = []
```

Session state maintains the chat history and metrics data across interactions.

#### Feature Demonstration Controls

```python
# Sidebar controls
query_type = st.radio(
    "What type of query do you want to make?",
    ["Investment Advice", "Loan Calculator", "Customer Service", "General Query"]
)

demo_modes = st.multiselect(
    "Select features to demonstrate",
    ["Rate Limiting", "Model Fallback", "Request Tracing", "Token Usage", "Latency Metrics"],
    default=["Token Usage", "Latency Metrics"]
)
```

These controls allow the demo presenter to showcase different features of the Envoy AI Gateway.

#### Metrics Visualization

```python
# Create token usage chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df["timestamp"],
    y=df["input_tokens"],
    name="Input Tokens",
    marker_color='#3B82F6'
))
fig.add_trace(go.Bar(
    x=df["timestamp"],
    y=df["output_tokens"],
    name="Output Tokens",
    marker_color='#10B981'
))
```

Interactive charts display token usage, latency, and request distribution metrics.

## Deployment and Infrastructure

### Docker Compose Setup

The application uses Docker Compose for easy deployment:

```yaml
services:
  envoy:
    image: envoyproxy/ai-gateway:v0.1.0
    container_name: envoy-ai-gateway
    volumes:
      - ./envoy_configs/envoy_config.yaml:/etc/envoy/envoy.yaml
    ports:
      - "9000:9000"  # API port
      - "9901:9901"  # Admin dashboard
```

Each component runs in its own container, with appropriate networking and volume mounts.

### Kubernetes Deployment (Production)

For production deployment, Kubernetes manifests would define:

1. **Deployment**: For each component (Envoy, ADK agents, etc.)
2. **Service**: For internal networking
3. **Ingress**: For external access
4. **ConfigMap**: For configuration data
5. **Secret**: For API keys and credentials

## Security Considerations

The implementation addresses security through:

1. **Authentication**: JWT validation for all API requests
2. **Authorization**: Role-based access control for different routes
3. **Rate Limiting**: Prevents abuse and controls costs
4. **Audit Logging**: Comprehensive request tracking for compliance
5. **CORS Policies**: Controls which domains can access the API

## Scaling Considerations

The architecture supports scaling through:

1. **Horizontal Scaling**: Multiple instances of each component
2. **Load Balancing**: Distribute traffic across instances
3. **Caching**: Semantic caching for common queries
4. **Fallbacks**: Handle service disruptions gracefully
5. **Observability**: Monitor performance and usage patterns

## Integration Points

The system can integrate with:

1. **Identity Providers**: For user authentication
2. **Financial Data APIs**: For real-time market data
3. **CRM Systems**: For customer context
4. **Compliance Systems**: For regulatory checks
5. **Monitoring Tools**: For operational visibility

## Conclusion

This implementation demonstrates how Envoy AI Gateway, Google ADK, and Streamlit can be combined to create a secure, scalable AI application for financial services. The architecture can be adapted for various domains where security, reliability, and specialized expertise are important.
