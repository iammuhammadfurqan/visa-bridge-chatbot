import streamlit as st
import time
from chatbot import VisaBridgeBot
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="VisaBridge AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: white;
    }
    .chat-message.bot {
        background-color: #f0f2f6;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
    }
    .chat-message .message {
        margin-top: 0.5rem;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = VisaBridgeBot()
    st.session_state.chatbot.start_conversation()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'conversation_summary' not in st.session_state:
    st.session_state.conversation_summary = None

# Sidebar
with st.sidebar:
    st.title("🤖 VisaBridge AI")
    st.markdown("---")
    
    # About section
    st.markdown("### About")
    st.markdown("""
    VisaBridge AI helps you navigate complex visa processes with:
    - Information for 20+ countries
    - Document requirements
    - Application procedures
    - Immigration guidance
    """)
    
    st.markdown("---")
    
    # Controls
    if st.button("Clear Conversation", key="clear_btn"):
        st.session_state.messages = []
        st.session_state.chatbot.clear_conversation()
        st.rerun()
    
    if st.button("Show Summary", key="summary_btn"):
        st.session_state.conversation_summary = st.session_state.chatbot.evaluator.generate_summary()
    
    # Display summary if available
    if st.session_state.conversation_summary:
        st.markdown("### Conversation Summary")
        st.json(st.session_state.conversation_summary)

# Main chat interface
st.title("VisaBridge AI Assistant")
st.markdown("Ask me anything about visa processes and immigration! I can understand queries in both English and Urdu (اردو).")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div style="display: flex; align-items: center;">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=user" class="avatar"/>
                    <div><strong>You</strong></div>
                </div>
                <div class="message">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot">
                <div style="display: flex; align-items: center;">
                    <img src="https://api.dicebear.com/7.x/bottts/svg?seed=bot" class="avatar"/>
                    <div><strong>VisaBridge AI</strong></div>
                </div>
                <div class="message">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
with st.container():
    # Create a form for the chat input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", placeholder="Type your question here...")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Show typing indicator
            with st.spinner("Thinking..."):
                # Get bot response
                response = st.session_state.chatbot.chat(user_input)
                
            # Add bot response to chat
            st.session_state.messages.append({"role": "bot", "content": response})
            
            # Rerun to update chat
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>VisaBridge AI Assistant | Powered by LangChain and OpenAI</p>
</div>
""", unsafe_allow_html=True)