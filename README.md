# Financial Advisor AI Gateway Demo

This demo showcases how to build a secure, scalable AI chatbot for financial advisory services using:

- **Envoy AI Gateway**: For secure routing, rate limiting, and observability
- **Google ADK (Agent Development Kit)**: For agent orchestration and specialized tasks
- **Streamlit**: For the user interface

## Business Case

Financial institutions need to provide personalized advisory services while:
- Protecting sensitive customer data
- Ensuring compliance with regulations
- Managing costs from multiple AI providers
- Routing different types of requests to appropriate models
- Providing consistent experiences across channels

This demo implements a financial advisor chatbot that securely routes requests to specialized models based on the query type (investment advice, loan calculations, customer service), while providing rate limiting and observability.

## Features Demonstrated

1. **Unified API Gateway**
   - Single entry point for multiple LLM providers
   - Standardized request/response format

2. **Intelligent Request Routing**
   - Route to appropriate model based on query type
   - Fallback logic when primary models are unavailable

3. **Rate Limiting and Token Usage**
   - Manage costs with token-based rate limiting
   - Track and report on usage

4. **Security and Observability**
   - Authentication and authorization
   - Request/response logging and monitoring
   - Anomaly detection

5. **Agent Orchestration**
   - Specialized agents for different financial tasks
   - Hierarchical delegation of requests

## Getting Started

See the [Installation Guide](docs/installation.md) to set up the demo.

## Project Structure

```
.
├── streamlit_app/        # Streamlit UI code
├── envoy_configs/        # Envoy AI Gateway configuration
├── agent_configs/        # Google ADK agent configurations
├── tools/                # Custom tools for financial calculations
└── docs/                 # Documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
