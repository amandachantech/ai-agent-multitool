# ai-agent-multitool/main.py
import streamlit as st
import pandas as pd
from langchain.memory import ConversationBufferMemory
from agents.chat_agent import ChatAgent
from agents.pdf_agent import PdfAgent
from agents.csv_agent import CsvAgent
from agents.router_agent import RouterAgent  
from utils.plot_utils import plot_bar, plot_line, plot_scatter


def render_history(messages: list[dict]):

    for msg in messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        st.chat_message(role).write(content)


st.set_page_config(page_title="Multi-Tool AI Agent", layout="wide")
st.title("🤖 Multi-Tool AI Agent")


st.sidebar.header("Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
mode = st.sidebar.radio("Mode", ["Smart Agent", "Chat", "PDF QA", "CSV QA"])


if mode == "Smart Agent":

    st.sidebar.subheader("Resources (Optional)")
    uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")
    uploaded_csv = st.sidebar.file_uploader("Upload CSV", type="csv")


    if "chat_mem" not in st.session_state:
        st.session_state["chat_mem"] = ConversationBufferMemory(return_messages=True)
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "Hi, I'm your AI assistant. How can I help you?"}
        ]

    if "smart_messages" not in st.session_state:
        st.session_state["smart_messages"] = [
            {"role": "assistant", "content": "Welcome to Smart Agent. Upload a PDF/CSV on the left or just ask a question."}
        ]


    df = None
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        st.dataframe(df, use_container_width=True)


    if "smart_pdf_memory" not in st.session_state:
        st.session_state["smart_pdf_memory"] = ConversationBufferMemory(
            return_messages=True, memory_key="chat_history", output_key="answer"
        )


    chat_agent = None
    pdf_agent = None
    csv_agent = None
    if api_key:
        chat_agent = ChatAgent(api_key, st.session_state["chat_mem"])
        if uploaded_pdf is not None:
            pdf_agent = PdfAgent(api_key, st.session_state["smart_pdf_memory"])
            pdf_agent.load_pdf(uploaded_pdf)
        if df is not None:
            csv_agent = CsvAgent(api_key, df)


    render_history(st.session_state["smart_messages"])


    user_query = st.chat_input("Describe your task or ask a question (the agent will pick a tool).")
    if user_query:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:

            st.session_state["smart_messages"].append({"role": "user", "content": user_query})

            st.chat_message("user").write(user_query)

            router = RouterAgent(chat_agent=chat_agent, pdf_agent=pdf_agent, csv_agent=csv_agent)
            resources = {
                "has_pdf": uploaded_pdf is not None,
                "has_csv": uploaded_csv is not None,
                "pdf_loaded": pdf_agent is not None,
                "csv_df": df,
            }

            with st.spinner("Selecting tool and generating response..."):
                result = router.route(user_query, resources)

            tool = result.get("tool", "chat")
            output = result.get("output", "")
            badge = f"**Selected tool:** `{tool.upper()}`\n\n"

            if tool == "chat":
                assistant_text = badge + (output or "")
                st.session_state["smart_messages"].append({"role": "assistant", "content": assistant_text})
                st.chat_message("assistant").write(assistant_text)

            elif tool == "pdf":
                ans = output.get("answer", "") if isinstance(output, dict) else ""
                assistant_text = badge + (ans or "(No answer)")
                st.session_state["smart_messages"].append({"role": "assistant", "content": assistant_text})
                st.chat_message("assistant").write(assistant_text)

            elif tool == "csv":
                ans = output.get("answer", "") if isinstance(output, dict) else ""
                assistant_text = badge + (ans or "Generated visualization or table.")
                st.session_state["smart_messages"].append({"role": "assistant", "content": assistant_text})
                st.chat_message("assistant").write(assistant_text)

                if isinstance(output, dict):
                    if "table" in output:
                        df_table = pd.DataFrame(output["table"]["data"], columns=output["table"]["columns"])
                        st.table(df_table)
                    if "bar" in output:
                        plot_bar(output["bar"])
                    if "line" in output:
                        plot_line(output["line"])
                    if "scatter" in output:
                        plot_scatter(output["scatter"])



elif mode == "Chat":
    if "chat_mem" not in st.session_state:
        st.session_state["chat_mem"] = ConversationBufferMemory(return_messages=True)
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "Hi, I'm your AI assistant. How can I help you?"}
        ]

    render_history(st.session_state["chat_messages"])

    user_input = st.chat_input("Type your message...")
    if user_input:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:
            agent = ChatAgent(api_key, st.session_state["chat_mem"])
            st.session_state["chat_messages"].append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            with st.spinner("Thinking..."):
                reply = agent.run(user_input)
            st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)


elif mode == "PDF QA":

    st.sidebar.subheader("PDF")
    uploaded_file = st.sidebar.file_uploader("Upload PDF file", type="pdf")

    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(
            return_messages=True, memory_key="chat_history", output_key="answer"
        )
    if "pdf_messages" not in st.session_state:
        st.session_state["pdf_messages"] = [
            {"role": "assistant", "content": "Upload a PDF on the left and ask a question about it."}
        ]


    render_history(st.session_state["pdf_messages"])


    question = st.chat_input("Enter your question about the uploaded PDF") if uploaded_file else None

    if uploaded_file and question:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:
            agent = PdfAgent(api_key, st.session_state["memory"])
            agent.load_pdf(uploaded_file)

            st.session_state["pdf_messages"].append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            with st.spinner("Generating answer..."):
                result = agent.run(question)

            answer = result.get("answer", "")
            st.session_state["pdf_messages"].append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)


elif mode == "CSV QA":
   
    st.sidebar.subheader("CSV")
    csv_file = st.sidebar.file_uploader("Upload CSV file", type="csv")

    if "csv_messages" not in st.session_state:
        st.session_state["csv_messages"] = [
            {"role": "assistant", "content": "Upload a CSV on the left and describe your analysis or visualization request."}
        ]

    df = None
    if csv_file:
        df = pd.read_csv(csv_file)
        st.dataframe(df, use_container_width=True)

    render_history(st.session_state["csv_messages"])

    query = st.chat_input("Enter query or visualization request") if df is not None else None

    if df is not None and query:
        if not api_key:
            st.warning("Please enter your OpenAI API Key.")
        else:
            st.session_state["csv_messages"].append({"role": "user", "content": query})
            st.chat_message("user").write(query)

            with st.spinner("Generating response..."):
                agent = CsvAgent(api_key, df)
                output = agent.run(query)

        
            if isinstance(output, dict) and "answer" in output:
                answer_text = output["answer"]
                st.session_state["csv_messages"].append({"role": "assistant", "content": answer_text})
                st.chat_message("assistant").write(answer_text)

          
            if isinstance(output, dict) and "table" in output:
                df_table = pd.DataFrame(output["table"]["data"], columns=output["table"]["columns"])
                st.table(df_table)
            if isinstance(output, dict) and "bar" in output:
                plot_bar(output["bar"])
            if isinstance(output, dict) and "line" in output:
                plot_line(output["line"])
            if isinstance(output, dict) and "scatter" in output:
                plot_scatter(output["scatter"])
