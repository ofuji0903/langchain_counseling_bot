import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from graph import app

st.set_page_config(
    page_title="カウンセリングチャットボット v3",
    page_icon="💬",
    layout="wide"
)

# スタイルの定義（テスト用）
st.markdown("""
    <style>
        div[class*="chat-message"] {
            background-color: red !important;
            border-radius: 8px;
            padding: 12px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 カウンセリングチャットボット v3")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
print("✅ CSS適用チェック: containerレンダリング実行")

# セッション状態の初期化
if "history" not in st.session_state:
    st.session_state.history = []

# ユーザー入力の処理
user_input = st.chat_input("あなたの話したいことを自由に書いてください:")

if user_input:
    # ユーザーメッセージの追加
    st.session_state.history.append({"role": "user", "message": user_input})
    
    # AIの応答を取得
    result = app.invoke({
        "user_input": user_input,
        "conversation_history": [item["message"] for item in st.session_state.history if item["role"] == "user"]
    })
    response = result["response"]
    
    # AIの応答を履歴に追加
    st.session_state.history.append({"role": "bot", "message": response})

# 最新10件のメッセージを表示
for item in st.session_state.history[-10:]:
    print(f"🔍 ログ: {item['role']} => {item['message']}")
    if item["role"] == "user":
        with st.chat_message("user"):
            st.markdown(item["message"])
    else:
        with st.chat_message("assistant"):
            st.markdown(item["message"])

st.markdown("</div>", unsafe_allow_html=True) 