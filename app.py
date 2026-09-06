import os
import streamlit as st
from retriever import build_rag_chain

st.set_page_config(
    page_title="Food Additive Compliance Auditor",
    page_icon="⚖️",
    layout="centered"
)

# Cache the RAG pipeline so it initializes only once on server boot
@st.cache_resource(show_spinner="Initializing Compliance Engine...")
def load_cached_chain():
    return build_rag_chain()

st.title("Food Additive Regulation Assistant")
st.caption("Grounded statutory verification powered by openai & FAISS")

rag_chain = load_cached_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Verified Statutory Citations"):
                for src in msg["sources"]:
                    st.markdown(src)

user_query = st.chat_input("Query statutory additive limits (e.g., 'Permissible sorbic acid in baked goods')")

if user_query:
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        try:
            response = rag_chain.invoke({"input": user_query})
            answer = response["answer"]
            sources = response.get("context", [])

            st.markdown(answer)

            # Citation extraction and formatting
            citation_records = []
            if sources:
                with st.expander("Verified Statutory Citations"):
                    for idx, doc in enumerate(sources, 1):
                        doc_name = os.path.basename(doc.metadata.get("source", "Regulation Corpus"))
                        page = doc.metadata.get("page", 0) + 1
                        citation = f"**[{idx}] {doc_name}** — *Page {page}*\n> {doc.page_content[:200]}..."
                        citation_records.append(citation)
                        st.markdown(citation)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": citation_records
            })

        except Exception as e:
            st.error(f"Inference Engine Error: {str(e)}")