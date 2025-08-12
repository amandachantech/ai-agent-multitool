# 🤖 Multi-Tool AI Agent

## 🚀 Project Overview
A **Streamlit** + **LangChain** based intelligent multi-tool AI Agent that automatically picks the right tool based on your query.  
It integrates three core features in a single **web app**:

1. **Smart Agent Mode** – Auto-routes between Chat, PDF QA, and CSV QA
2. **PDF Question Answering** – RAG-based document Q&A
3. **CSV Data Analysis & Visualization**

This project demonstrates **modular AI tool integration** with a user-friendly interface, deployable locally or in the cloud. Perfect for portfolio demos and educational purposes.

---

## 🎬 Demo Video
https://www.loom.com/share/99a8bad9c1d341c3a7f5d7bb743ef3a2?sid=0d9835e4-09af-4664-9d3c-6dfc78e941c6

---

## 📂 Project Structure

```text
ai-agent-multitool/
├── agents/
│   ├── chat_agent.py         # Chat mode
│   ├── pdf_agent.py          # PDF QA
│   ├── csv_agent.py          # CSV QA & visualization
│   └── router_agent.py       # Tool routing logic
├── utils/
│   ├── chat_utils.py         # Chat memory helpers
│   ├── pdf_utils.py          # PDF processing & retrieval
│   ├── csv_utils.py          # DataFrame queries
│   └── plot_utils.py         # Chart rendering
├── main.py                   # Streamlit entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Features

### 1. Smart Agent Mode
- Automatically selects Chat, PDF QA, or CSV QA.
- Supports simultaneous PDF & CSV uploads with persistent conversation history.

### 2. PDF QA
- Upload PDF → Text chunking → FAISS vector search → RAG-powered Q&A.
- Ideal for document summarization and section-level retrieval.

### 3. CSV QA
- Upload CSV → Ask in natural language.
- Automatically generates answers, tables, bar charts, line charts, and scatter plots.

---

## 🛠️ Installation & Run

```bash
git clone https://github.com/<your_account>/ai-agent-multitool.git
cd ai-agent-multitool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```
Open browser at [http://localhost:8501](http://localhost:8501)

---

## 🚀 How to Use

1. **Enter OpenAI API Key in the sidebar**
2. **Choose mode** (Smart Agent / Chat / PDF QA / CSV QA)
3. **Upload PDF or CSV (optional)**
4. **Type your query** – results will appear instantly, with visualizations when applicable.

---

## 📈 Possible Enhancements
- Support more file types (Word, image OCR)
- Multi-provider LLM selection (OpenAI, DeepSeek…)
- Deploy on Streamlit Cloud or Docker

---
## 👋 About Me
I'm an AI Engineer passionate about building multi-tool AI agents and scalable RAG pipelines.  
Currently exploring opportunities to contribute to cutting-edge AI agent frameworks and infrastructure.

## 📄 Resume
You can download my latest resume here: [AmandaChan_Resume.pdf](./AmandaChan_Resume.pdf)

## 📬 Contact
- Email: [amandachan.tech@gmail.com](mailto:amandachan.tech@gmail.com)
