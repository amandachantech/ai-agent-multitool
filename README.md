# 🤖 Multi-Tool AI Agent

A multi-functional intelligent agent powered by **ChatGPT**, designed to handle:

- 💬 **General conversation**  
- 📄 **PDF document question-answering** (retrieval-based QA)  
- 📊 **CSV data analysis and visualization**  

All features are integrated into a unified **Streamlit web interface**.

---

## 🚀 Features

✅ **Chat Mode** – Context-aware conversation with memory  
✅ **PDF QA** – Upload a PDF and ask questions, powered by FAISS retrieval  
✅ **CSV QA** – Analyze and visualize CSV data with automatic charts and tables  
✅ **Interactive Web UI** – Simple, responsive interface built with Streamlit  
✅ **LangChain-powered Agents** – Modular agents for extensibility  

---

## 🛠️ Project Structure

```
ai-agent-multitool/
│── agents/
│   ├── chat_agent.py      # Handles general chat
│   ├── pdf_agent.py       # Handles PDF document QA
│   └── csv_agent.py       # Handles CSV data analysis
│
│── utils/
│   ├── chat_utils.py      # Chat memory and response utilities
│   ├── csv_utils.py       # CSV DataFrame agent utilities
│   ├── pdf_utils.py       # PDF loader, splitter, FAISS retriever
│   └── plot_utils.py      # Chart plotting utilities for Streamlit
│
│── main.py                # Streamlit app entry point
│── requirements.txt
│── README.md
```

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-agent-multitool.git
   cd ai-agent-multitool
   ```

2. **Create and activate a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. **Start the Streamlit application**
   ```bash
   streamlit run main.py
   ```

2. **Open the app** in your browser (usually `http://localhost:8501`)  

3. **Select a mode** from the sidebar:
   - **Chat:** Type messages and chat with the AI.  
   - **PDF QA:** Upload a PDF and ask context-based questions.  
   - **CSV QA:** Upload a CSV and request data analysis or visualizations.

---

## ⚙️ Tech Stack

- **[OpenAI GPT models](https://platform.openai.com/)** – AI-powered responses  
- **[LangChain](https://www.langchain.com/)** – Agent orchestration  
- **[FAISS](https://github.com/facebookresearch/faiss)** – Vector search for PDFs  
- **[Streamlit](https://streamlit.io/)** – Interactive web UI  
- **Pandas & Matplotlib** – Data handling and visualization  

---

## 📌 Future Improvements

- 🔹 Support for multi-file PDF QA  
- 🔹 Advanced charting options  
- 🔹 Session export/import  
- 🔹 Deployment to cloud platforms (Streamlit Sharing / Docker)

---

## 📄 Resume
You can download my latest resume here: [AmandaChan_Resume.pdf](./AmandaChan_Resume.pdf)
