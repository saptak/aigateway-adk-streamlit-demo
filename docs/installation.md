# Installation Guide

This guide will walk you through setting up the Financial Advisor AI Gateway Demo.

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- kubectl (if deploying to Kubernetes)
- A Google Cloud account (for ADK integration)
- API keys for LLM providers (OpenAI, Anthropic, etc.)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/aigateway-adk-streamlit-demo.git
cd aigateway-adk-streamlit-demo
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with your API keys:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
```

### 3. Install Dependencies

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Envoy AI Gateway

Using Docker:

```bash
docker-compose up -d envoy
```

Or manually:

```bash
cd envoy_configs
envoy -c envoy_config.yaml
```

### 5. Start the Google ADK Agents

```bash
cd agent_configs
python start_agents.py
```

### 6. Launch the Streamlit App

```bash
cd streamlit_app
streamlit run app.py
```

### 7. Access the Demo

Open your browser and navigate to:
- Streamlit UI: http://localhost:8501
- Envoy Dashboard: http://localhost:9901

## Configuration Options

### Envoy AI Gateway Configuration

The demo uses a basic configuration. To modify:

1. Edit `envoy_configs/envoy_config.yaml`
2. Restart the Envoy process or container

### Google ADK Agent Configuration

To modify the agent behavior:

1. Edit files in the `agent_configs` directory
2. Restart the agent process

### Streamlit UI Configuration

To customize the UI:

1. Edit files in the `streamlit_app` directory
2. The changes will be applied automatically when you refresh the page

## Troubleshooting

### Common Issues

1. **API Rate Limiting**: If you encounter rate limiting issues, check your API usage and consider adjusting the rate limits in the Envoy configuration.

2. **Connection Refused**: Ensure all services are running. Check Docker container status with `docker ps`.

3. **Authentication Errors**: Verify your API keys are correctly set in the `.env` file.

For more assistance, please open an issue on the GitHub repository.
