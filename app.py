import streamlit as st

from src.loader import load_pdf
from src.splitter import split_documents
from src.vectorstore import create_vectorstore
from src.qa_chain import create_qa_chain

st.set_page_config(page_title="Multi PDF ChatBot")

st.title("📚 Chat with Multiple PDFs")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload PDFs
uploaded_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:

    all_docs = []

    with st.spinner("Processing PDFs..."):

        for uploaded_file in uploaded_files:

            # Save uploaded file temporarily
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Load PDF
            docs = load_pdf(uploaded_file.name)

            # Debug information
            st.write(f"### File: {uploaded_file.name}")
            st.write("Number of pages:", len(docs))

            if len(docs) > 0:
                st.write("### First Page Content")
                st.write(docs[0].page_content[:1000])

            # Add docs to master list
            all_docs.extend(docs)

        # Split documents
        chunks = split_documents(all_docs)

        st.write("Total Chunks Created:", len(chunks))

        # Create vector database
        vector_store = create_vectorstore(chunks)

        # Create LLM + Retriever
        llm, retriever = create_qa_chain(vector_store)

    st.success(f"{len(uploaded_files)} PDF(s) processed successfully!")

    # Display previous chats
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question from the PDFs")

    if question:

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Retrieve relevant chunks
        relevant_docs = retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        # Show retrieved text for debugging
        st.write("### Retrieved Context")
        st.write(context[:2000])

        chat_history = ""

        for msg in st.session_state.messages:
            chat_history += f"{msg['role']}: {msg['content']}\n"

        prompt = f"""
You are an AI assistant.

Answer ONLY from the provided context.

If the answer is not found in the context, say:
'I could not find the answer in the uploaded PDFs.'

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""

        response = llm.invoke(prompt)

        answer = response.content

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

            st.markdown("### Source Pages")

            pages = []

            for doc in relevant_docs:
                if "page" in doc.metadata:
                    pages.append(doc.metadata["page"] + 1)

            pages = sorted(list(set(pages)))

            for page in pages:
                st.write(f"📄 Page {page}")