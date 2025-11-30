import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Health Advice Chatbot",
    page_icon="🏥",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f1f8e9;
        border-left: 4px solid #8bc34a;
    }
    .stButton > button {
        width: 100%;
        background-color: #2196f3;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #1976d2;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:5001/health-advice"

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🏥 Health Advice Chatbot")
st.markdown("Ask me anything about health conditions, medications, or dietary advice!")
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br/>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Health Assistant:</strong><br/>
            {content}
        </div>
        """, unsafe_allow_html=True)

# Input area
with st.container():
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your question:",
            key="user_input",
            placeholder="e.g., What are the side effects of aspirin?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", type="primary")

# Handle user input
if send_button and user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show loading spinner
    with st.spinner("Thinking..."):
        try:
            # Call Flask API
            response = requests.post(
                API_URL,
                json={"prompt": user_input},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "No response received")
                
                # Add bot response to chat history
                st.session_state.messages.append({"role": "bot", "content": bot_response})
            else:
                error_message = f"Error: {response.status_code} - {response.text}"
                st.session_state.messages.append({"role": "bot", "content": error_message})
        
        except requests.exceptions.Timeout:
            st.session_state.messages.append({
                "role": "bot",
                "content": "⚠️ Request timed out. Please try again."
            })
        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "bot",
                "content": "⚠️ Could not connect to the API. Make sure the Flask server is running on port 5001."
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "bot",
                "content": f"⚠️ An error occurred: {str(e)}"
            })
    
    # Rerun to update the chat display
    st.rerun()

# Sidebar with additional info
with st.sidebar:
    st.header("ℹ️ Information")
    st.markdown("""
    This chatbot provides health advice using AI-powered agents.
    
    **Features:**
    - Medical precautions
    - Side effect information
    - Dietary recommendations
    - Health summaries
    
    **Tips:**
    - Be specific with your questions
    - Mention patient names if applicable
    - Ask about medications, conditions, or general health advice
    """)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**API Status**")
    try:
        health_check = requests.get("http://localhost:5001/health", timeout=2)
        if health_check.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Powered by ARK AI Agents</div>",
    unsafe_allow_html=True
)
