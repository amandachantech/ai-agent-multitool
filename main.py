# ai-agent-multitool/main.py
import streamlit as st
import pandas as pd
from langchain.memory import ConversationBufferMemory
from agents.chat_agent import ChatAgent
from agents.pdf_agent import PdfAgent
from agents.csv_agent import CsvAgent
from utils.plot_utils import plot_bar, plot_line, plot_scatter

# Set up the page configuration
st.set_page_config(page_title="Multi-Tool AI Agent", layout="wide")
st.title("🤖 Multi-Tool AI Agent")

# Sidebar: API Key and mode selection
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
mode = st.sidebar.radio("Select Functionality", ["Chat", "PDF QA", "CSV QA"])

# --- CHAT MODE ---
if mode == "Chat":
    # Initialize memory and chat message history
    if "chat_mem" not in st.session_state:
        st.session_state["chat_mem"] = ConversationBufferMemory(return_messages=True)
        st.session_state["chat_messages"] = [{"role": "assistant", "content": "Hello, I am your AI assistant. How can I help you today?"}]
    
    # Display chat history
    for msg in st.session_state["chat_messages"]:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # User input field
    user_input = st.chat_input("Type your message...")
    if user_input:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:
            agent = ChatAgent(api_key, st.session_state["chat_mem"])
            st.chat_message("user").write(user_input)
            with st.spinner("AI is generating a response..."):
                reply = agent.run(user_input)
            # Update and display AI response
            st.session_state["chat_messages"].append({"role": "user", "content": user_input})
            st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)

# --- PDF QA MODE ---
elif mode == "PDF QA":
    # Initialize PDF memory and chat history
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer"
        )
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # File upload and question input
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    question = st.text_input("Enter your question", disabled=not uploaded_file)

    if uploaded_file and question:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:
            agent = PdfAgent(api_key, st.session_state["memory"])
            agent.load_pdf(uploaded_file)
            with st.spinner("AI is generating a response..."):
                result = agent.run(question)
            # Display answer
            st.write("### Answer")
            st.write(result.get("answer", ""))
            # Update chat history
            st.session_state["chat_history"] = result.get("chat_history", [])
    
    # Display chat history
    if st.session_state["chat_history"]:
        with st.expander("Conversation History"):
            for i in range(0, len(st.session_state["chat_history"]), 2):
                human_message = st.session_state["chat_history"][i]
                ai_message = st.session_state["chat_history"][i + 1]
                st.write(human_message.content)
                st.write(ai_message.content)
                if i < len(st.session_state["chat_history"]) - 2:
                    st.divider()

# --- CSV QA MODE ---
elif mode == "CSV QA":
    csv_file = st.file_uploader("Upload CSV file", type="csv")
    df = None
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df)
    
    query = st.text_area("Enter your query or visualization request")
    if st.button("Submit") and df is not None and query:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:
            with st.spinner("AI is processing..."):
                agent = CsvAgent(api_key, df)
                output = agent.run(query)
            # Display text answer
            if "answer" in output:
                st.write(output["answer"])
            # Display table
            if "table" in output:
                df_table = pd.DataFrame(output["table"]["data"], columns=output["table"]["columns"])
                st.table(df_table)
            # Display charts
            if "bar" in output:
                plot_bar(output["bar"])
            if "line" in output:
                plot_line(output["line"])
            if "scatter" in output:
                plot_scatter(output["scatter"])
