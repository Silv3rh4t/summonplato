import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

load_dotenv()


embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
db = FAISS.load_local("faiss_index/plato", embedding, allow_dangerous_deserialization=True)


llm = ChatOpenAI(
    model="qwen/qwen3-30b-a3b:free", 
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

def get_context(question: str, k: int = 3) -> list[Document]:
    return db.similarity_search(question, k=k)

def format_prompt(context_docs: list[Document], question: str) -> str:
    context = "\n\n---\n\n".join(doc.page_content for doc in context_docs)
    return f"""You are Plato. Answer the following question based on the context provided.

Context:
{context}

Question:
{question}

Answer like a philosopher, clearly and thoughtfully."""

if __name__ == "__main__":
    while True:
        user_q = input("\nAsk Plato: ")
        if user_q.strip().lower() in {"exit", "quit"}:
            break
        docs = get_context(user_q)
        prompt = format_prompt(docs, user_q)
        response = llm.invoke(prompt)
        print(f"\n Plato says:\n{response}")
