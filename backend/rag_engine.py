import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGEngine:
    def __init__(self, pdf_dir="pdfs", index_path="rag_index"):
        self.pdf_dir = pdf_dir
        self.index_path = index_path
        
        # 1. Latest Embedding Model (Warning Free)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vector_db = None
        self.load_or_build_index()

    def load_or_build_index(self):
        """
        Agar index pehle se hai toh load karega, varna build karega.
        """
        if os.path.exists(self.index_path):
            print("[RAG] Loading existing index...")
            self.vector_db = FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            print("[RAG] Index loaded successfully.")
        else:
            self.build_index()

    def build_index(self):
        """
        PDFs ko read karke naya FAISS index banata hai.
        """
        print("[RAG] Building new index from PDFs...")
        
        # Folder check
        if not os.path.exists(self.pdf_dir):
            os.makedirs(self.pdf_dir)
            print(f"[RAG] Warning: '{self.pdf_dir}' folder nahi mila. Khali folder bana diya hai.")
            return

        # Load PDFs
        loader = DirectoryLoader(self.pdf_dir, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()

        if not docs:
            print("[RAG] Error: 'pdfs' folder mein koi PDF nahi mili!")
            return

        # Text Splitter (Small chunks for better search)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
        final_docs = text_splitter.split_documents(docs)

        # Create and Save Index
        self.vector_db = FAISS.from_documents(final_docs, self.embeddings)
        self.vector_db.save_local(self.index_path)
        print(f"[RAG] Index built with {len(final_docs)} chunks and saved locally.")

    def search(self, query, k=3):
        """
        User ke sawal ke liye relevant context dhoondta hai.
        """
        if not self.vector_db:
            return "No context available (PDFs not loaded)."
        
        # Similarity search
        results = self.vector_db.similarity_search(query, k=k)
        context = "\n".join([doc.page_content for doc in results])
        return context