import os
import pickle
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "pdfs"
INDEX_PATH = BASE_DIR / "rag_index"


class RAGEngine:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstore = None

    def build_index(self):
        print("[RAG] Building new index...")

        documents = []

        for file in os.listdir(PDF_DIR):
            if file.lower().endswith(".pdf"):
                pdf_path = PDF_DIR / file
                loader = PyPDFLoader(str(pdf_path))
                docs = loader.load()
                documents.extend(docs)
                print(f"[RAG] Loaded {file}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

        chunks = splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)

        self.vectorstore.save_local(str(INDEX_PATH))
        print("[RAG] Index built & saved")

    def load_or_build(self):
        if (INDEX_PATH / "index.faiss").exists():
            print("[RAG] Loading existing index...")
            self.vectorstore = FAISS.load_local(
                str(INDEX_PATH),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("[RAG] Index loaded")
        else:
            self.build_index()

    def search(self, query, k=4):
        if self.vectorstore is None:
            self.load_or_build()

        results = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in results])


# global instance jo main.py import karega
rag_engine = RAGEngine()
