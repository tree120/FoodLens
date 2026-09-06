FoodLens --- Food Additive Regulation Assistant

FoodLens is an AI-powered regulatory compliance assistant for querying
food-additive regulations. It uses Retrieval-Augmented Generation (RAG)
to retrieve relevant information from regulatory PDF documents and
generate grounded answers with statutory source references.

Features

PDF-based regulatory document ingestion

PyPDFLoader for loading regulatory PDFs

RecursiveCharacterTextSplitter for creating searchable chunks

Hugging Face embeddings using
sentence-transformers/all-MiniLM-L6-v2

FAISS vector store for semantic retrieval

MMR/similarity-based retrieval

Groq-hosted LLM for answer generation

Grounded responses that avoid unsupported claims

Document and page-level source citations

Streamlit web interface

Conversation-style question and answer interface

RAG Pipeline

Regulatory PDFs
      ↓
PyPDFLoader
      ↓
Text Splitting
      ↓
Hugging Face Embeddings
      ↓
FAISS Vector Store
      ↓
Retriever
      ↓
Groq LLM
      ↓
Grounded Answer + Sources

Project Structure

FoodLens/
│
├── app.py                    # Streamlit application
├── retriever.py              # RAG retrieval and question-answering logic
├── ingest.py                 # PDF ingestion and FAISS index creation
├── requirements.txt          # Project dependencies
├── pyproject.toml            # uv project/dependency configuration
├── .env                      # API keys (do not commit)
├── .gitignore
│
├── data/
│   └── *.pdf                 # Regulatory PDF documents
│
└── vectorstore/
    └── db_faiss/             # Generated FAISS index

File names such as ingest.py can be changed to match the actual
project files.

Requirements

Python 3.13+

uv

A Groq API key

Internet access for downloading the embedding model the first time

Installation

1. Clone the repository

git clone <your-repository-url>
cd FoodLens

2. Create a virtual environment

uv venv

Activate it on Git Bash:

source .venv/Scripts/activate

On PowerShell:

.venv\Scripts\Activate.ps1

3. Install dependencies

If using requirements.txt:

uv pip install -r requirements.txt

For Windows environments where hard-linking causes an access error, use:

uv pip install --link-mode=copy -r requirements.txt

Alternatively, if dependencies are declared in pyproject.toml:

uv sync

Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

Never commit .env or expose your API key publicly.

Building the Vector Store

Place the regulatory PDF files inside the data/ directory.

Then run the ingestion script:

uv run ingest.py

This process:

Loads the PDF files.

Splits the documents into smaller chunks.

Generates embeddings for the chunks.

Stores the embeddings in FAISS.

Saves the vector store under vectorstore/db_faiss.

Running the Application

Start the Streamlit application with:

uv run streamlit run app.py

Then open the local URL shown by Streamlit, usually:

http://localhost:8501

Do not run a Streamlit application with:

uv run app.py

Use streamlit run so Streamlit can create its application context and
session state correctly.

Example Questions

You can test FoodLens with questions such as:

What does INS number mean?

Is sodium benzoate permitted in fruit juice?

What is the maximum permitted level of sodium benzoate in fruit
juice?

What are the permitted uses of citric acid (INS 330)?

What is the maximum permitted level of potassium sorbate (INS 202)?

Are there any restrictions on the use of artificial colors?

What happens if an additive exceeds its permitted limit?

For questions whose answer is not supported by the provided regulatory
documents, the assistant is designed to indicate that the information
could not be verified from the available regulations rather than
inventing an answer.

Grounded Responses

FoodLens is designed to answer using the retrieved regulatory context.

The prompt instructs the model to:

Answer only from the provided context.

Give a direct answer first.

Avoid unsupported assumptions.

Report permitted levels only when explicitly supported.

Provide document and page references when available.

Avoid health or safety claims unless they are present in the
supplied regulatory context.

Technologies Used

Technology                           Purpose

Python                               Application development
LangChain                            RAG orchestration
LangChain Community                  PDF loading and FAISS integration
LangChain Hugging Face               Embedding integration
Hugging Face Sentence Transformers   Text embeddings
FAISS                                Vector similarity search
Groq                                 LLM inference
Streamlit                            Web interface
uv                                   Python package and project management

Important Notes

Virtual Environment

The .venv directory isolates project dependencies from the global
Python environment. This prevents package-version conflicts between
projects.

uv

uv is used to manage the Python environment and dependencies. For
project dependencies, prefer:

uv add package-name

For installing an existing requirements.txt:

uv pip install -r requirements.txt

FAISS Vector Store

The FAISS database is generated from the regulatory PDFs. If the source
documents change, rebuild the vector store so that the index reflects
the updated documents.

Embedding Model

The same embedding model should be used when creating and loading the
FAISS vector store:

sentence-transformers/all-MiniLM-L6-v2

Security

Do not commit API keys or secrets.

Make sure .gitignore contains:

.env
.venv/
__pycache__/
*.pyc

Future Improvements

OCR support for scanned regulatory documents

Image/product-label upload

Automatic extraction of food additive names and INS numbers

Better citation display

Hybrid keyword + semantic retrieval

Re-ranking of retrieved regulatory passages

User authentication

Deployment to a cloud platform

Automated regulatory document updates

Disclaimer

FoodLens is an educational/software project intended to assist with
searching and understanding the provided regulatory documents. It should
not be treated as a substitute for official legal, regulatory, medical,
or professional compliance advice.
