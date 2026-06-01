import html
import streamlit as st
import pandas as pd
from chatbot import CustomerSupportBot

st.set_page_config(page_title="Electronix Support", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    /* Main background */
    .stApp {
        background: linear-gradient(145deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #131826;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #6c63ff, #a855f7);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 0;
        transition: all 0.2s;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.4);
    }

    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }

    /* Message rows */
    .user-row, .bot-row {
        display: flex;
        margin: 12px 0;
        animation: fadeIn 0.3s ease;
    }
    .user-row { justify-content: flex-end; }
    .bot-row { justify-content: flex-start; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Bubble base */
    .bubble {
        max-width: 75%;
        padding: 14px 18px;
        border-radius: 20px;
        font-size: 14px;
        line-height: 1.5;
        word-wrap: break-word;
    }

    /* User bubble */
    .user-bubble {
        background: linear-gradient(135deg, #6c63ff, #a855f7);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 0 2px 8px rgba(108, 99, 255, 0.25);
    }

    /* Bot bubble */
    .bot-bubble {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        color: #e2e8f0;
        border-bottom-left-radius: 4px;
    }

    /* Avatar */
    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin: 0 10px;
    }
    .user-avatar {
        background: linear-gradient(135deg, #6c63ff, #a855f7);
        color: white;
        order: 2;
    }
    .bot-avatar {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        color: #a855f7;
    }

    /* Input */
    div[data-baseweb="input"] input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(108,99,255,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    div[data-baseweb="input"] input:focus {
        border-color: #6c63ff !important;
        box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.15) !important;
    }
    div[data-baseweb="input"] input::placeholder {
        color: rgba(255,255,255,0.3) !important;
    }

    /* Send button */
    .stButton button[kind="secondary"] {
        background: linear-gradient(135deg, #6c63ff, #a855f7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 4px 20px !important;
        height: 48px;
    }

    /* Quick reply chips */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 8px 0;
    }
    .chip-container button {
        background: rgba(108, 99, 255, 0.15) !important;
        border: 1px solid rgba(108, 99, 255, 0.3) !important;
        color: #c4b5fd !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }
    .chip-container button:hover {
        background: rgba(108, 99, 255, 0.3) !important;
        border-color: #6c63ff !important;
        color: white !important;
    }

    /* Header */
    .header-container {
        text-align: center;
        padding: 20px 0 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #c4b5fd, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .header-sub {
        font-size: 14px;
        color: rgba(255,255,255,0.5);
        margin-top: 4px;
    }

    /* Subtle background blur shapes */
    .bg-shapes {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }
    .bg-shapes .shape {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.08;
    }
    .bg-shapes .shape-1 {
        width: 400px; height: 400px;
        background: #6c63ff;
        top: -100px; right: -100px;
    }
    .bg-shapes .shape-2 {
        width: 300px; height: 300px;
        background: #a855f7;
        bottom: -50px; left: -80px;
    }
    .bg-shapes .shape-3 {
        width: 250px; height: 250px;
        background: #3b82f6;
        top: 40%; left: 20%;
    }

    /* Chat scroll area */
    .chat-scroll {
        max-height: 55vh;
        overflow-y: auto;
        padding-right: 8px;
    }
    .chat-scroll::-webkit-scrollbar {
        width: 4px;
    }
    .chat-scroll::-webkit-scrollbar-track {
        background: transparent;
    }
    .chat-scroll::-webkit-scrollbar-thumb {
        background: rgba(108,99,255,0.3);
        border-radius: 4px;
    }

    /* metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 16px;
    }
    div[data-testid="metric-container"] label {
        color: rgba(255,255,255,0.5) !important;
    }
    div[data-testid="metric-container"] div {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bg-shapes">
    <div class="shape shape-1"></div>
    <div class="shape shape-2"></div>
    <div class="shape shape-3"></div>
</div>
""", unsafe_allow_html=True)

if "bot" not in st.session_state:
    st.session_state.bot = CustomerSupportBot()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0
if "category_counts" not in st.session_state:
    st.session_state.category_counts = {}
if "session_started" not in st.session_state:
    st.session_state.session_started = False

def start_session():
    if not st.session_state.session_started:
        st.session_state.session_started = True
        st.session_state.conversation_count += 1
        greeting = st.session_state.bot.get_response("Hello")
        st.session_state.messages.append({"role": "bot", "content": greeting["response"], "intent": greeting["intent"]})

def handle_send():
    user_msg = st.session_state.user_input.strip()
    if user_msg and user_msg not in [m["content"] for m in st.session_state.messages if m["role"] == "user"]:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        reply = st.session_state.bot.get_response(user_msg)
        st.session_state.messages.append({"role": "bot", "content": reply["response"], "intent": reply["intent"]})
        intent_display = st.session_state.bot.get_category_name(reply["intent"])
        st.session_state.category_counts[intent_display] = st.session_state.category_counts.get(intent_display, 0) + 1
    st.session_state.user_input = ""

def handle_chip(msg):
    st.session_state.messages.append({"role": "user", "content": msg})
    reply = st.session_state.bot.get_response(msg)
    st.session_state.messages.append({"role": "bot", "content": reply["response"], "intent": reply["intent"]})
    intent_display = st.session_state.bot.get_category_name(reply["intent"])
    st.session_state.category_counts[intent_display] = st.session_state.category_counts.get(intent_display, 0) + 1

def clear_chat():
    st.session_state.messages = []
    st.session_state.session_started = False

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#c4b5fd; font-weight:700; margin-bottom:20px;'>📊 Analytics</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Conversations", st.session_state.conversation_count)
    with col2:
        if st.session_state.category_counts:
            top_cat = max(st.session_state.category_counts, key=st.session_state.category_counts.get)
            st.metric("Top Category", top_cat)
        else:
            st.metric("Top Category", "—")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:rgba(255,255,255,0.6); font-size:14px; font-weight:600;'>Category Breakdown</h3>", unsafe_allow_html=True)
    if st.session_state.category_counts:
        df = pd.DataFrame(
            list(st.session_state.category_counts.items()),
            columns=["Category", "Count"]
        ).sort_values("Count", ascending=False)
        for _, row in df.iterrows():
            pct = row["Count"] / sum(st.session_state.category_counts.values()) * 100
            st.markdown(
                f"<div style='margin:6px 0;'>"
                f"<div style='display:flex; justify-content:space-between; font-size:13px; color:#e2e8f0;'>"
                f"<span>{row['Category']}</span><span>{row['Count']}</span>"
                f"</div>"
                f"<div style='background:rgba(255,255,255,0.06); border-radius:4px; height:6px;'>"
                f"<div style='background:linear-gradient(90deg,#6c63ff,#a855f7); width:{pct}%; height:6px; border-radius:4px;'></div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown("<p style='color:rgba(255,255,255,0.3); font-size:13px;'>No data yet. Start chatting!</p>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin:20px 0;'>", unsafe_allow_html=True)
    st.button("🗑️ Clear Chat", on_click=clear_chat, use_container_width=True)

# Main header
st.markdown("""
<div class="header-container">
    <div class="header-title">⚡ Electronix Support</div>
    <div class="header-sub">AI-powered customer care — ask me anything about your orders or products</div>
</div>
""", unsafe_allow_html=True)

# Start session if not started
if not st.session_state.session_started:
    start_session()

# Chat display
st.markdown('<div class="chat-container chat-scroll">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-row">'
            f'<div class="bubble user-bubble">{html.escape(msg["content"])}</div>'
            f'<div class="avatar user-avatar">👤</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-row">'
            f'<div class="avatar bot-avatar">🤖</div>'
            f'<div class="bubble bot-bubble">'
            f'{msg["content"]}'
            f'<br><span style="font-size:11px;color:rgba(255,255,255,0.25);">'
            f'— {st.session_state.bot.get_category_name(msg.get("intent",""))}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Quick reply chips
st.markdown('<div class="chip-container">', unsafe_allow_html=True)
suggestions = st.session_state.bot.get_suggestions()
for s in suggestions:
    if st.button(s, key=f"chip_{s}", use_container_width=False):
        handle_chip(s)
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Input area
with st.container():
    col_in, col_btn = st.columns([5, 1])
    with col_in:
        st.text_input(
            "Message",
            key="user_input",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            on_change=handle_send,
        )
    with col_btn:
        st.button("Send", on_click=handle_send, type="secondary", use_container_width=True)
