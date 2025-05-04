FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent config files
COPY ./agent_configs /app

ENTRYPOINT ["python", "start_agents.py"]
