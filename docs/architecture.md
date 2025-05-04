# Financial Advisor AI Gateway Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                         │
│                                                                     │
│  ┌─────────────────────────┐                                        │
│  │    Streamlit UI         │                                        │
│  │                         │                                        │
│  │  - Chat Interface       │                                        │
│  │  - Configuration        │                                        │
│  │  - Metrics Visualization│                                        │
│  └──────────────┬──────────┘                                        │
└──────────────────┼──────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Gateway Layer                               │
│                                                                     │
│  ┌─────────────────────────┐                                        │
│  │    Envoy AI Gateway     │                                        │
│  │                         │                                        │
│  │  - Routing              │                                        │
│  │  - Rate Limiting        │                                        │
│  │  - Authentication       │                                        │
│  │  - Model Fallbacks      │                                        │
│  │  - Observability        │                                        │
│  └──────────────┬──────────┘                                        │
└──────────────────┼──────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Agent Layer                                 │
│                                                                     │
│  ┌─────────────────────────┐                                        │
│  │    Google ADK           │                                        │
│  │    Coordinator Agent    │                                        │
│  │                         │                                        │
│  │  - Query Understanding  │                                        │
│  │  - Task Routing         │                                        │
│  │  - Response Synthesis   │                                        │
│  └──────────────┬──────────┘                                        │
│                 │                                                   │
│     ┌───────────┴───────────┬───────────────────┐                   │
│     ▼                       ▼                   ▼                   │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────────┐      │
│  │ Investment  │      │ Loan         │     │ Customer       │      │
│  │ Advisor     │      │ Specialist   │     │ Service        │      │
│  │ Agent       │      │ Agent        │     │ Agent          │      │
│  └─────┬───────┘      └──────┬───────┘     └────────┬───────┘      │
└─────────┼────────────────────┼─────────────────────┼────────────────┘
           │                    │                     │
           ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Tool Layer                                  │
│                                                                     │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────────┐      │
│  │ Investment  │      │ Loan         │     │ Information    │      │
│  │ Calculator  │      │ Calculator   │     │ Retrieval      │      │
│  └─────────────┘      └──────────────┘     └────────────────┘      │
│                                                                     │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────────┐      │
│  │ Stock Data  │      │ Mortgage     │     │ Google         │      │
│  │ API         │      │ Calculator   │     │ Search         │      │
│  └─────────────┘      └──────────────┘     └────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
           │                    │                     │
           ▼                    ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Model Layer                                 │
│                                                                     │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────────┐      │
│  │ OpenAI      │      │ Anthropic    │     │ Google         │      │
│  │ GPT-4       │      │ Claude 3     │     │ Gemini         │      │
│  └─────────────┘      └──────────────┘     └────────────────┘      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Interactions

### Request Flow

1. User enters a query in the Streamlit UI
2. UI sends the request to Envoy AI Gateway
3. Gateway authenticates request and applies rate limiting
4. Gateway routes request to appropriate endpoint based on query type
5. ADK Coordinator Agent receives the request
6. Coordinator analyzes the request and routes to specialized agents
7. Specialized agent uses tools to process the request
8. Agent generates response using appropriate LLM
9. Response flows back through the chain
10. UI displays response and updates metrics

### Data Flow

```
┌───────────┐    Query     ┌───────────┐    Routed    ┌───────────┐
│           │──────────────►           │──────────────►           │
│ Streamlit │              │  Envoy    │              │  Google   │
│    UI     │◄──────────────  Gateway  │◄──────────────   ADK     │
│           │   Response   │           │   Response   │           │
└───────────┘              └───────────┘              └───────────┘
                                                           │
                                                           │
                                                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Tool Access                              │
│                                                                  │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────────┐   │
│  │ Financial   │      │ External     │     │ Internal       │   │
│  │ Calculators │      │ APIs         │     │ Knowledge Base │   │
│  └─────────────┘      └──────────────┘     └────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

## Key Metrics and Monitoring Points

```
┌───────────────────────┐
│   Gateway Metrics     │
├───────────────────────┤
│ - Request Volume      │
│ - Token Usage         │
│ - Latency             │
│ - Error Rate          │
│ - Model Fallbacks     │
│ - Rate Limit Events   │
└───────────────────────┘

┌───────────────────────┐
│   Agent Metrics       │
├───────────────────────┤
│ - Agent Routing       │
│ - Task Success Rate   │
│ - Tool Usage          │
│ - Processing Time     │
└───────────────────────┘

┌───────────────────────┐
│   Security Metrics    │
├───────────────────────┤
│ - Auth Failures       │
│ - Suspicious Patterns │
│ - PII Detection       │
│ - Compliance Checks   │
└───────────────────────┘
```

This architecture provides a scalable, secure foundation for building AI-powered financial advisory services with multiple layers of redundancy, observability, and specialization.
