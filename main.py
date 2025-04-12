import os
import streamlit as st
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI  # ← 最新構成ではここ
# ※ langchain_community も使うなら別途 import

# .envの読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY が .env に設定されていません")
    st.stop()

# LLMとメモリの設定
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_key=api_key
)

memory = ConversationBufferMemory()

# LangChainで会話チェーン作成
chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Streamlit UI
st.title("LangChain カウンセリングチャットボット")

user_input = st.text_input("あなた: ", "")

if user_input:
    response = chain.run(user_input)
    st.write(f"カウンセラー: {response}")
