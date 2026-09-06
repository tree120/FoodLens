import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

DB_FAISS_PATH = "vectorstore/db_faiss"

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    return FAISS.load_local(
        DB_FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

def build_rag_chain():
    vectorstore = load_vectorstore()

    # Deterministic inference for regulatory compliance
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.1,
        max_tokens=512,
        api_key=os.environ.get("GROQ_API_KEY")
    )

    # Maximal Marginal Relevance (MMR) for diverse, non-redundant chunk retrieval
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10}
    )


    # system_prompt = (
    #     "You are an expert regulatory compliance auditor for food additives.\n"
    #     "Answer the user's question STRICTLY using the context below. If the permissible "
    #     "limits, INS numbers, or statutory rules are not explicitly mentioned in the context, "
    #     "state clearly that the provided regulatory documentation does not contain this information. "
    #     "Do NOT extrapolate or assume.\n\n"
    #     "Context:\n{context}"
    # )

    system_prompt = (
        "You are a friendly, helpful guide explaining food additive rules and safety.\n\n"
        "Your goal is to explain things in simple, everyday language so anyone can understand, "
        "without sounding like a dry legal or technical document. Break down complicated terms, "
        "use short bullet points when listing numbers or limits, and keep your tone warm and conversational.\n\n"
        "Important rules:\n"
        "1. Base your answer strictly on the context provided below.\n"
        "2. If the document doesn't mention the answer or specific limits, just say warmly: "
        "'I couldn't find that specific information in the regulations provided.' Never guess or make up numbers.\n"
        "3. Highlight key numbers (like permissible limits) clearly so they are easy to spot at a glance.\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, combine_docs_chain)

if __name__ == "__main__":
    chain = build_rag_chain()
    test_query = input("Enter regulatory query to test: ")
    res = chain.invoke({"input": test_query})
    
    print("\n--- COMPLIANCE ANSWER ---")
    print(res["answer"])
    print("\n--- VERIFIED SOURCES ---")
    for doc in res["context"]:
        src = os.path.basename(doc.metadata.get("source", "Unknown"))
        page = doc.metadata.get("page", 0) + 1
        print(f"- {src} (Page {page})")