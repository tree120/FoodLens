# 🍎 FoodLens

## 🤖 AI-Powered Food Additive Regulatory Assistant

FoodLens is a RAG-based regulatory compliance chatbot that helps users ask natural-language questions about food-additive regulations. It retrieves relevant information from regulatory PDF documents and generates source-grounded answers with document and page references.

## 🎯 Main Goal

The main goal of FoodLens is to make complex food-additive regulations easier to understand and access, especially for ordinary consumers.

Instead of reading large and complicated regulatory documents, users can simply ask questions such as:

"What does INS 211 mean?"

"Is sodium benzoate permitted in fruit juice?"

The chatbot searches the provided regulatory documents and returns the relevant information with supporting sources.

## 👥 Who Can Use FoodLens?

FoodLens can be useful for:

• 🛒 Consumers who want to understand food additives and INS numbers
• 🏭 Food manufacturers who need quick access to additive regulations
• 🧪 Food technologists working with food formulation
• ✅ Quality and compliance teams
• 🔬 Researchers and students studying food regulations

## 🏗️ Architecture

FoodLens follows a Retrieval-Augmented Generation (RAG) architecture.

Document Processing:

Regulatory PDF Documents
↓
PyPDFLoader
↓
Text Chunking
↓
Hugging Face Embeddings
↓
FAISS Vector Store

Question Answering:

User Question
↓
Query Embedding
↓
FAISS Retriever
↓
Relevant Regulatory Context
↓
Groq LLM
↓
Grounded Answer
↓
Document and Page Reference

## 🔄 How It Works

1. 📄 Regulatory PDF documents are loaded using PyPDFLoader.
2. ✂️ The extracted text is divided into smaller chunks using RecursiveCharacterTextSplitter.
3. 🧠 Each chunk is converted into a vector using a Hugging Face embedding model.
4. 🗂️ The vectors are stored in FAISS.
5. 🔎 When a user asks a question, the question is converted into an embedding.
6. 🎯 FAISS retrieves the most relevant regulatory chunks.
7. 📚 The retrieved context is passed to the Groq LLM.
8. 🤖 The LLM generates an answer using the retrieved context.
9. 📌 The chatbot displays the answer along with document and page references.

## 🧠 Key Design Decisions

### 🔍 Retrieval-Augmented Generation

RAG was chosen because the chatbot needs to answer questions using specific regulatory documents rather than relying only on the LLM's general knowledge.

This approach also helps reduce unsupported or hallucinated regulatory claims.

### ✂️ Document Chunking

RecursiveCharacterTextSplitter is used to divide large documents into smaller chunks while maintaining overlap between chunks.

Current configuration:

chunk_size: 1000
chunk_overlap: 150

Document source and page information are preserved to support traceability.

### 🧠 Embedding Model

FoodLens uses:

sentence-transformers/all-MiniLM-L6-v2

This model converts documents and user questions into numerical vectors for semantic retrieval.

### 🔎 Vector Search

FAISS is used for vector similarity search.

Current retrieval configuration:

k = 4
fetch_k = 10

MMR retrieval can be used to reduce redundancy among retrieved chunks.

### 🤖 Language Model

FoodLens uses:

openai/gpt-oss-20b

The model is accessed through the Groq API and generates the final answer using the retrieved regulatory context.

## 📌 Grounded Answers

FoodLens is designed to prefer verifiable information over unsupported guesses.

The chatbot is instructed to:

• ✅ Answer using the retrieved regulatory context
• ✅ Avoid unsupported assumptions
• ✅ Avoid inventing regulatory limits
• ✅ Clearly state when information is not available
• ✅ Provide document and page references when available

## 🛠️ Tech Stack

Python 3.13+ — Core application development

LangChain — RAG pipeline and orchestration

PyPDF / PyPDFLoader — PDF processing

RecursiveCharacterTextSplitter — Document chunking

Hugging Face — Embedding generation

Sentence Transformers — Semantic embeddings

FAISS — Vector storage and retrieval

Groq API — LLM inference

GPT-OSS 20B — Language model

Streamlit — User interface

uv — Environment and dependency management

python-dotenv — Environment variable management

## 🤖 Models Used

### 🧠 Embedding Model

sentence-transformers/all-MiniLM-L6-v2

Used to generate embeddings for regulatory documents and user questions.

### 💬 Language Model

openai/gpt-oss-20b

Used to generate the final response from the retrieved regulatory context.

## 🔑 API Used

FoodLens uses the Groq API for LLM inference.

The API key is stored in a .env file:

GROQ_API_KEY=your_groq_api_key_here

The API key should never be committed to GitHub or exposed publicly.

## 📚 Knowledge Source

The current knowledge base consists of food-additive regulatory PDF documents.

Example:

data/
└── Food_Additives_Regulations.pdf

These documents are processed and converted into a FAISS vector store before they are used for question answering.

## 🎯 Scope

The current version focuses on food-additive regulatory information contained in the provided documents.

Users can ask about:

• 🧪 Food additives
• 🔢 INS numbers
• ✅ Permitted uses
• 🍎 Food categories
• 📏 Maximum permitted levels
• 📋 Regulatory restrictions
• 📖 Other information available in the indexed documents



## 🚀 Future Improvements

### 📷 OCR and Image Support

Add OCR support so consumers can upload or photograph food labels.

Food Label Image
↓
OCR
↓
Ingredients and Additives
↓
INS Numbers
↓
Regulatory Retrieval

### 🏷️ Product Verification

The system could automatically detect additives from a food label and compare them with the relevant regulatory requirements.

Product Label
↓
OCR / Information Extraction
↓
Detected Additives
↓
Regulatory Retrieval
↓
Limit Comparison
↓
Compliance Result
↓
Supporting Evidence

### 🔎 Improved Retrieval

Future versions could include:

• Hybrid keyword and semantic search
• Metadata filtering
• Retrieval re-ranking
• Better handling of regulatory tables
• Improved chunking strategies

### 🌍 Expanded Regulatory Coverage

Support regulatory documents from multiple authorities, countries, and jurisdictions.

### 📊 Compliance Reports

Generate reports containing:

• Product information
• Detected additives
• Regulatory limits
• Compliance status
• Supporting sources

### 🔄 Automatic Updates

Automatically process updated regulatory documents so the knowledge base stays current.

## ▶️ Quick Start

Create the virtual environment:

uv venv

Activate the environment in Git Bash:

source .venv/Scripts/activate

Install dependencies:

uv pip install -r requirements.txt

For Windows hard-link or cloud-sync issues:

uv pip install --link-mode=copy -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here

Place regulatory PDFs inside:

data/

Build the FAISS vector store:

uv run ingest.py

Start the Streamlit application:

uv run streamlit run app.py

Open the application:

[http://localhost:8501](http://localhost:8501)

## 🔒 Security

Never commit API keys, secrets, or virtual environments.

Recommended .gitignore entries:

.env
.venv/
**pycache**/
*.pyc

## ⚠️ Disclaimer

FoodLens is an educational software project designed to help users search and understand the provided regulatory documents.

It is not a substitute for official regulations, legal advice, regulatory advice, medical advice, or professional compliance review.

Important regulatory decisions should always be verified against the latest official and authoritative sources.
