# Production_RAG_Project

A Production RAG Chatbot built using **LangChain, Groq, Qdrant, and Streamlit**.

## Features

* Chat with PDF documents
* Supports multiple PDF files
* Semantic search using Qdrant
* OCR support for scanned PDFs
* Streamlit-based interactive UI

## Tech Stack

* Python
* LangChain
* Groq
* Qdrant
* Streamlit
* PyTesseract
* PDF2Image

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shrishtypriya2006-rgb/Production_RAG_Project.git
```

### 2. Move into the project folder

```bash
cd Production_RAG_Project
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

Add your Groq API key inside the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 7. Run the application

```bash
streamlit run app.py
```

## Project Structure

```text
Production_RAG_Project/
│
├── src/
│   ├── __init__.py
│   ├── loader.py
│   ├── splitter.py
│   ├── vectorstore.py
│   └── qa_chain.py
│
├── app.py
├── test.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Author

**Shrishty Priya**
