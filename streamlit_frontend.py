import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# ✅ Correct config
CONFIG = {"configurable": {"thread_id": "thread-1"}}

with st.chat_message('assistant'):
    st.text("Hi, Welcome to Graph Mate ! ")

# ✅ Fix typo in session state key
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# ✅ Render old messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# ✅ Chat input
user_input = st.chat_input("Type here...")

if user_input:
    # Save user message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.text(user_input)

    # Call chatbot
    response = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]}, config=CONFIG
    )

    ai_message = response["messages"][-1].content

    # Save AI response
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )

    with st.chat_message("assistant"):
        st.text(ai_message)
