import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()


def create_qa_chain(vector_store):

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return llm, retriever