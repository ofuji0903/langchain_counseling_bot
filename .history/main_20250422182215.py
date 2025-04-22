# main.py
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from graph import app  # ← Graphは別ファイルで定義

# ページ設定
st.set_page_config(
    page_title="カウンセリングチャットボット v3",
    page_icon="💬"
)

# カスタムCSS
st.markdown("""
<style>
    .main {
        max-width: 800px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #e6f7ff;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.title("カウンセリングチャットボット v3")

# サイドバー（信頼度ゲージ用のスペース確保）
with st.sidebar:
    st.markdown("### 信頼度")
    st.progress(0.7)  # ダミーの信頼度ゲージ

# チャット履歴の初期化
if "history" not in st.session_state:
    st.session_state.history = []

# チャット履歴の表示
for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

# チャット入力
user_input = st.chat_input("あなたの話したいことを自由に書いてください:")

if user_input:
    conversation_history = [msg[0] for msg in st.session_state.history]
    result = app.invoke({
        "user_input": user_input,
        "conversation_history": conversation_history
    })
    response = result["response"]

    st.session_state.history.append((user_input, response))

    # 最新のメッセージを表示
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(response)

if st.session_state.history:
    st.markdown("---")
    st.markdown("#### 過去の会話")
    for user_msg, bot_msg in reversed(st.session_state.history[-5:]):
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(bot_msg)
