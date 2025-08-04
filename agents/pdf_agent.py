# agents/pdf_agent.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from utils.pdf_utils import load_pdf_to_retriever

class PdfAgent:
    """
    PDF Question-Answering Agent.
    Loads a PDF document, builds a retriever, and enables conversational retrieval-based QA.
    """
    def __init__(self, api_key: str, memory: ConversationBufferMemory):
        """
        Initialize the PdfAgent.

        Args:
            api_key (str): OpenAI API key.
            memory (ConversationBufferMemory): Memory for tracking conversation history.
        """
        self.api_key = api_key
        self.memory = memory
        # Initialize the chat model instance
        self.model = ChatOpenAI(
            model="gpt-4.1-nano-2025-04-14",
            openai_api_key=api_key
        )
        self.chain = None

    def load_pdf(self, uploaded_file):
        """
        Load a PDF file, split it into chunks, build a FAISS retriever,
        and create a ConversationalRetrievalChain.

        Args:
            uploaded_file: The PDF file to be processed.
        """
        retriever = load_pdf_to_retriever(
            uploaded_file=uploaded_file,
            api_key=self.api_key
        )
        # Combine retriever and memory into a conversational retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.model,
            retriever=retriever,
            memory=self.memory
        )
  
    def run(self, question: str) -> dict:
        """
        Execute the retrieval chain to generate an answer and return updated conversation history.

        Args:
            question (str): The user's question related to the PDF content.

        Returns:
            dict: {
                "answer": "<response text>",
                "chat_history": [<HumanMessage>, <AIMessage>, …]
            }
        """
        if self.chain is None:
            raise ValueError("Please call load_pdf() before running the retrieval chain.")

        # Pass only the question; the chain internally uses retriever and memory
        answer = self.chain.run(question)

        # Retrieve the complete chat history from memory
        history = self.memory.load_memory_variables({}).get("chat_history", [])

        return {"answer": answer, "chat_history": history}
