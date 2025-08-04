# utils/pdf_utils.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def load_pdf_to_retriever(
    uploaded_file,
    api_key: str,
    temp_path: str = "temp.pdf",
    chunk_size: int = 1000,
    chunk_overlap: int = 50
) -> FAISS:
    """
    Load an uploaded PDF file and build a FAISS-based retriever for document search.

    Args:
        uploaded_file: File object uploaded via Streamlit or similar file uploader.
        api_key (str): OpenAI API key.
        temp_path (str): Temporary file path for storing the uploaded PDF.
        chunk_size (int): Size of each text chunk for splitting the document.
        chunk_overlap (int): Overlap size between consecutive text chunks.

    Returns:
        FAISS retriever instance ready for semantic search.
    """
    # Save the uploaded PDF to a temporary path
    content = uploaded_file.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    # Load the document using PyPDFLoader
    loader = PyPDFLoader(temp_path)
    docs = loader.load()

    # Split document into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    texts = text_splitter.split_documents(docs)

    # Create embeddings and build a FAISS index
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    faiss_db = FAISS.from_documents(texts, embeddings)

    # Remove the temporary file
    try:
        os.remove(temp_path)
    except OSError:
        pass

    # Return the retriever
    return faiss_db.as_retriever()
