from src.loader import load_pdf
from src.splitter import split_documents
from src.vectorstore import create_vectorstore
from src.qa_chain import create_qa_chain

# Load PDF
docs = load_pdf("Project_Report_Final.pdf")

print("Number of pages:", len(docs))

# Split PDF into chunks
chunks = split_documents(docs)

print("Number of chunks:", len(chunks))

# Create vector store
vector_store = create_vectorstore(chunks)

print("Vector Store Created Successfully!")

# Create LLM and retriever
llm, retriever = create_qa_chain(vector_store)

# Ask user question
query = input("\nAsk a question from the PDF: ")

# Retrieve relevant chunks
relevant_docs = retriever.invoke(query)

# Create context
context = "\n".join([doc.page_content for doc in relevant_docs])

# Create prompt
prompt = f"""
Answer the question only using the context given below.

Context:
{context}

Question:
{query}
"""

# Get response from LLM
response = llm.invoke(prompt)

print("\nAnswer:\n")
print(response.content)