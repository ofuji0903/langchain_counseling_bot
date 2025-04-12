import streamlit as st
from chains.stage_router_chain import get_stage
from chains.response_chain import generate_response
from chains.rag_interface import retrieve_knowledge

st.set_page_config(page_title="カウンセリングチャットボット v2", page_icon="💬")
st.title("カウンセリングチャットボット v2")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("あなたの話したいことを自由に書いてください:")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    stage = get_stage(user_input)
    context = retrieve_knowledge(stage, user_input)
    response = generate_response(stage, user_input, context)

    st.session_state.history.append((user_input, response, stage))

    with st.chat_message("assistant"):
        st.markdown(response)

if st.session_state.history:
    st.markdown("---")
    st.markdown("#### 過去の会話")
    for user_msg, bot_msg, stage in reversed(st.session_state.history[-5:]):
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(bot_msg)