import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/"
DB_FAISS_PATH = "vectorStore/db_faiss"

# 1. Batch Load All Regulatory Documents
def load_regulatory_corpus(data_dir: str):
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")
    
    loader = DirectoryLoader(
        data_dir,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True
    )
    return loader.load()

# 2. Semantic Chunking with Legal/Regulatory Clause Retention
def create_regulatory_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,          # ~150-200 words: preserves full statutory rules
        chunk_overlap=150,        # Prevents clause truncation across chunk seams
        separators=["\n\n", "\n", "(?=[A-Z0-9]+\\.)", " ", ""], # Splits on structured numbering
        is_separator_regex=True
    )
    chunks = text_splitter.split_documents(documents)
    
    # Inject source & page metadata directly into chunk prefix to preserve context
    for chunk in chunks:
        doc_source = os.path.basename(chunk.metadata.get("source", "Unknown"))
        page_num = chunk.metadata.get("page", 0) + 1
        chunk.page_content = f"Document: {doc_source} | Page: {page_num}\n" + chunk.page_content
        
    return chunks

# 3. Vector Embeddings
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True} # Critical for cosine similarity in FAISS
    )

def build_vector_store():
    docs = load_regulatory_corpus(DATA_PATH)
    chunks = create_regulatory_chunks(docs)
    embeddings = get_embedding_model()
    
    # 4. Generate & Save FAISS Index
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"Indexed {len(chunks)} chunks across {len(docs)} pages to {DB_FAISS_PATH}")

if __name__ == "__main__":
    build_vector_store()