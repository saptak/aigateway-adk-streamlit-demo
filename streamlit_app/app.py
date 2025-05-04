import streamlit as st
import requests
import json
import os
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:9000")
API_KEY = os.getenv("API_KEY", "demo-key")

# Page configuration
st.set_page_config(
    page_title="Financial Advisor AI Gateway Demo",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
    }
    .subheader {
        font-size: 1.5rem;
        color: #3B82F6;
    }
    .feature-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #E2E8F0;
    }
    .ai-message {
        background-color: #DBEAFE;
    }
    .info-box {
        background-color: #FEF3C7;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #F59E0B;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "token_usage" not in st.session_state:
    st.session_state.token_usage = {"input": 0, "output": 0}

if "request_history" not in st.session_state:
    # Store timestamp, request_type, model, latency, tokens
    st.session_state.request_history = []

if "last_route" not in st.session_state:
    st.session_state.last_route = None

# Sidebar
with st.sidebar:
    st.markdown("## Financial Advisor Demo")
    st.image("https://via.placeholder.com/150x150.png?text=AI+Gateway", width=150)
    
    st.markdown("### Configure Demo")
    
    query_type = st.radio(
        "What type of query do you want to make?",
        ["Investment Advice", "Loan Calculator", "Customer Service", "General Query"]
    )
    
    # Map query type to API routes
    route_mapping = {
        "Investment Advice": "/v1/investment",
        "Loan Calculator": "/v1/loan",
        "Customer Service": "/v1/customer",
        "General Query": "/v1/general"
    }
    
    st.markdown("### Demo Features")
    demo_modes = st.multiselect(
        "Select features to demonstrate",
        ["Rate Limiting", "Model Fallback", "Request Tracing", "Token Usage", "Latency Metrics"],
        default=["Token Usage", "Latency Metrics"]
    )
    
    st.markdown("### Stats")
    st.metric("Input Tokens Used", st.session_state.token_usage["input"])
    st.metric("Output Tokens Used", st.session_state.token_usage["output"])
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.token_usage = {"input": 0, "output": 0}
        st.session_state.request_history = []
        st.session_state.last_route = None
        st.experimental_rerun()

# Main content
st.markdown('<p class="main-header">Financial Advisor AI Gateway Demo</p>', unsafe_allow_html=True)

# Show feature info box based on selected demo mode
if demo_modes:
    features_text = ", ".join(demo_modes)
    st.markdown(f'<div class="info-box">Currently demonstrating: {features_text}</div>', unsafe_allow_html=True)

# Two-column layout for chat and metrics
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="subheader">Chat with your Financial Advisor</p>', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_query = st.text_input("Ask a financial question:", key="user_input")
    
    if user_query:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Prepare request based on query type
        current_route = route_mapping[query_type]
        st.session_state.last_route = current_route
        
        # Record start time for latency tracking
        start_time = time.time()
        
        try:
            # Make request to AI Gateway
            response = requests.post(
                f"{GATEWAY_URL}{current_route}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                json={"prompt": user_query, "demo_modes": demo_modes}
            )
            
            # Calculate latency
            latency = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract metrics
                token_usage = result.get("usage", {"input_tokens": 0, "output_tokens": 0})
                st.session_state.token_usage["input"] += token_usage.get("input_tokens", 0)
                st.session_state.token_usage["output"] += token_usage.get("output_tokens", 0)
                
                # Add response to chat
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
                
                # Record request history
                st.session_state.request_history.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "request_type": query_type,
                    "model": result.get("model", "unknown"),
                    "latency": round(latency, 2),
                    "input_tokens": token_usage.get("input_tokens", 0),
                    "output_tokens": token_usage.get("output_tokens", 0)
                })
                
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
                # Record error in history
                st.session_state.request_history.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "request_type": query_type,
                    "model": "error",
                    "latency": round(latency, 2),
                    "input_tokens": 0,
                    "output_tokens": 0
                })
                
        except Exception as e:
            error_msg = f"Connection error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Force UI to update
        st.experimental_rerun()

with col2:
    st.markdown('<p class="subheader">Gateway Metrics</p>', unsafe_allow_html=True)
    
    if "Token Usage" in demo_modes and st.session_state.request_history:
        st.markdown("#### Token Usage Over Time")
        
        # Create dataframes for token usage
        df = pd.DataFrame(st.session_state.request_history)
        
        if not df.empty:
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
            
            fig.update_layout(
                barmode='group',
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    if "Latency Metrics" in demo_modes and st.session_state.request_history:
        st.markdown("#### Latency by Model")
        
        df = pd.DataFrame(st.session_state.request_history)
        
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["latency"],
                mode='lines+markers',
                name="Latency (s)",
                marker_color='#F59E0B'
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                yaxis_title="Seconds",
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    if "Request Tracing" in demo_modes and st.session_state.request_history:
        st.markdown("#### Request Routing")
        
        df = pd.DataFrame(st.session_state.request_history)
        
        if not df.empty:
            # Count request types
            request_counts = df["request_type"].value_counts().reset_index()
            request_counts.columns = ["Request Type", "Count"]
            
            fig = go.Figure(data=[go.Pie(
                labels=request_counts["Request Type"],
                values=request_counts["Count"],
                hole=.4,
                marker_colors=['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
            )])
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Display raw requests data in an expandable section
    if st.session_state.request_history:
        with st.expander("View Request History"):
            st.dataframe(pd.DataFrame(st.session_state.request_history))
