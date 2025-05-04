# Financial Advisor AI Gateway Demo Script

## Introduction (2-3 minutes)

Hello everyone! Today, I'm excited to demonstrate how Envoy AI Gateway, Google's Agent Development Kit, and Streamlit can be combined to create a secure, scalable AI application for financial services.

### The Business Problem

Financial institutions face several challenges when implementing AI solutions:

1. **AI Provider Dependency**: Relying on a single LLM provider creates vendor lock-in and single points of failure
2. **Cost Management**: LLM usage costs can escalate quickly without proper controls
3. **Security Concerns**: Financial data is sensitive and requires strict security measures
4. **Specialized Knowledge**: Different financial queries require different types of expertise
5. **Observability**: Tracking and analyzing AI usage patterns is crucial for optimization

### Our Solution

We've created a Financial Advisor chatbot that addresses these challenges using:

- **Envoy AI Gateway**: To manage traffic between our application and multiple LLM providers
- **Google ADK**: To orchestrate specialized AI agents for different financial tasks
- **Streamlit**: For a user-friendly interface that demonstrates key features
- **Ollama (Optional)**: For running models locally to minimize costs

## Demo Walkthrough (10-15 minutes)

### 1. Architecture Overview (2 minutes)

Let me start by explaining the high-level architecture:

[*Show architecture diagram from slides or draw on whiteboard*]

- **Frontend Layer**: Streamlit provides the user interface
- **Gateway Layer**: Envoy AI Gateway manages traffic to different LLM providers
- **Agent Layer**: Google ADK orchestrates specialized financial agents
- **Model Layer**: Multiple LLM providers (OpenAI, Anthropic, Google) or local models via Ollama

### 2. Key Features Demo (10 minutes)

Let's look at the application and see these features in action.

#### 2.1 Unified API and Request Routing

*[Navigate to the demo app in the browser]*

"Our Streamlit interface allows users to interact with a financial advisor chatbot. Behind the scenes, Envoy AI Gateway routes requests to the appropriate models based on the query type."

*[Show the sidebar settings]*

"Here, we can select the type of financial query we want to make. Let's start with an investment question."

*[Select "Investment Advice" and ask a question like: "How should I allocate my retirement portfolio if I'm 35 years old?"]*

"Notice how this investment query was routed to OpenAI's GPT-4. The gateway determined this was an investment query and directed it to our investment-specialized model."

*[Now select "Loan Calculator" and ask: "What would my monthly payment be for a $300,000 mortgage over 30 years at 4.5% interest?"]*

"This time, the gateway recognized a loan calculation query and routed it to a model that has been fine-tuned for numerical accuracy."

*[Point out the routing information in the metrics panel]*

"The request routing panel shows how queries are distributed across different query types."

#### 2.2 Local Model Inference with Ollama

*[Switch to "Local (Ollama)" in the sidebar]*

"Now let's switch to local model inference using Ollama. This option lets you run models on your own hardware, eliminating API costs while still getting quality responses."

*[Select "llama3-8b" from the model dropdown]*

"We're now using Llama 3 8B, a powerful open-source model running locally. Let's ask a similar investment question."

*[Ask another investment question]*

"Notice the response still provides helpful financial advice, but look at the latency metrics - local models typically respond faster but with potentially different response quality compared to API models."

*[Point out the "Local" tag on the response]*

"The UI displays which model generated each response, making it easy to compare cloud and local performance."

*[Switch back to "Cloud APIs" for comparison]*

"By providing both options, financial institutions can use cloud APIs for critical customer-facing applications while using local models for internal tools, testing, or cost-sensitive scenarios."

#### 2.3 Rate Limiting and Usage Tracking

*[Enable "Rate Limiting" and "Token Usage" in the demo features]*

"Envoy AI Gateway provides token-based rate limiting to control costs. Let's enable these features to see them in action."

*[Ask several questions in quick succession]*

"The token usage graph shows how many tokens we're consuming for each request, both input (prompts) and output (responses). This helps organizations monitor and control their AI spending."

*[If a rate limit message appears]*: "We've hit our simulated rate limit! In a production environment, you can configure these limits based on user roles, departments, or other criteria."

#### 2.4 Model Fallbacks

*[Enable "Model Fallback" in the demo features]*

"What happens if our primary model provider has an outage or latency issues? Let's enable the fallback demo to see."

*[Ask a few more questions]*

"Notice how one of our requests was automatically routed to our fallback model when the primary was simulated to be unavailable. This provides resilience without any changes to the client application."

"In the metrics panel, you can see which provider actually handled each request."

#### 2.5 Observability and Analytics

*[Enable "Request Tracing" and "Latency Metrics"]*

"Envoy AI Gateway provides comprehensive observability features. Let's enable request tracing and latency metrics."

*[Ask a few more questions of different types]*

"The metrics panel now shows us latency for each model, helping us identify performance issues. The request history table provides a detailed audit trail of all requests, which is especially important in regulated industries like financial services."

### 3. Google ADK Agent Orchestration (3 minutes)

"Behind the scenes, Google's Agent Development Kit orchestrates specialized agents for different financial tasks. Let's see this in action."

*[Ask a complex financial question that spans multiple domains, like: "I have $50,000 to invest, but I also have a mortgage. Should I invest the money or pay down my mortgage faster?"]*

"This question requires both investment knowledge and loan calculation. Our coordinator agent understands this complexity and routes parts of the query to specialized agents, then combines their responses into a cohesive answer."

"The ADK gives us a framework for building hierarchical agents that can tackle complex, multi-domain problems while maintaining context."

## Technical Implementation (3-5 minutes)

Let me briefly explain the key components of our implementation:

### 1. Envoy AI Gateway Configuration

*[Show envoy_config.yaml and envoy_config_ollama.yaml]*

"The Envoy AI Gateway configuration defines our API routes, rate limits, security policies, and model providers. It uses a declarative YAML format that's easy to understand and modify."

"We have two configurations:
- The standard config uses cloud-based API models
- The Ollama config adds support for local model inference"

"Key sections include:
- Route definitions for different query types
- Rate limit configurations based on tokens
- Fallback logic for high availability
- Security policies including JWT authentication
- Observability settings for logging and metrics"

### 2. Google ADK Agent Implementation

*[Show agent_definitions.py]*

"Our ADK implementation defines specialized agents for investment advice, loan calculations, and customer service. Each agent has:
- A specific model configuration
- Custom instructions
- Specialized tools like financial calculators
- A defined scope of responsibility"

"The coordinator agent decides which specialized agent should handle each request based on the query content, enabling a divide-and-conquer approach to complex financial questions."

### 3. Streamlit UI with Local Model Support

*[Show app.py]*

"Our Streamlit application provides an intuitive UI with just a few hundred lines of Python code. It includes:
- A chat interface for interacting with the financial advisor
- Real-time metrics visualization using Plotly
- Configuration options to demonstrate different features
- A toggle between cloud APIs and local models
- A responsive layout that works on different devices"

## Business Benefits (2 minutes)

This architecture delivers significant business benefits for financial institutions:

1. **Cost Optimization**: 
   - Token-based rate limiting and usage tracking help control API costs
   - Local model inference eliminates API fees for suitable use cases

2. **High Availability**: 
   - Model fallbacks ensure service continuity during outages
   - Mix of cloud and local options provides redundancy

3. **Vendor Independence**: 
   - Support for multiple AI providers prevents lock-in
   - Open-source options reduce dependency on commercial services

4. **Security**: 
   - Centralized authentication, authorization, and audit logging
   - Option to keep sensitive data on-premises with local models

5. **Performance Optimization**: 
   - Latency tracking helps identify and resolve bottlenecks
   - Local models can offer lower latency for certain applications

6. **Compliance**: 
   - Request tracing provides audit trails for regulatory requirements
   - Local inference can address data sovereignty concerns

## Conclusion (1 minute)

The combination of Envoy AI Gateway, Google ADK, Streamlit, and Ollama provides a powerful foundation for building secure, scalable, and cost-effective AI applications in financial services and beyond.

This architecture pattern can be applied to various domains where security, cost control, and specialized expertise are important requirements.

Thank you for your attention! I'm happy to answer any questions.

## Q&A (As needed)

[Be prepared to answer questions about implementation details, scalability, security, integration with existing systems, etc.]
