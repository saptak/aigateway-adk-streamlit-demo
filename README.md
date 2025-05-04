# Financial Advisor AI Gateway Demo

This demo showcases how to build a secure, scalable AI chatbot for financial advisory services using:

- **Envoy AI Gateway**: For secure routing, rate limiting, and observability
- **Google ADK (Agent Development Kit)**: For agent orchestration and specialized tasks
- **Streamlit**: For the user interface
- **Ollama**: For local model inference to minimize costs

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
   - Support for both cloud APIs and local models

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

6. **Cost Optimization with Local Models**
   - Option to use Ollama for local model inference
   - Compare performance between cloud and local models
   - No API fees for local model usage

## Getting Started

See the [Installation Guide](docs/installation.md) to set up the demo.

For setting up Ollama for local model inference, see the [Ollama Setup Guide](docs/ollama_setup.md).

## Project Structure

```
.
├── streamlit_app/        # Streamlit UI code
├── envoy_configs/        # Envoy AI Gateway configuration
│   ├── envoy_config.yaml # Cloud API configuration
│   └── envoy_config_ollama.yaml # Configuration with Ollama support
├── agent_configs/        # Google ADK agent configurations
├── tools/                # Custom tools for financial calculations
└── docs/                 # Documentation
    ├── installation.md   # Installation instructions
    ├── ollama_setup.md   # Ollama setup guide
    └── technical_details.md # Detailed implementation explanation
```

## Cloud vs. Local Models

This demo provides two deployment options:

1. **Cloud API Models**:
   - Use OpenAI, Anthropic, and Google models
   - Higher quality responses
   - Requires API keys and internet connection
   - Incurs usage costs

2. **Local Models (via Ollama)**:
   - Run models on your own hardware
   - No API fees
   - Works offline
   - May require powerful hardware for larger models

You can easily switch between these options in the Streamlit UI to compare performance, quality, and latency.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
