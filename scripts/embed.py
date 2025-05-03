import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Directories
CLEAN_DIR = Path(__file__).resolve().parent.parent / "data/cleaned"
INDEX_DIR = Path(__file__).resolve().parent.parent / "faiss_index/plato"
INDEX_DIR.parent.mkdir(parents=True, exist_ok=True)

# Embedder
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en",
    model_kwargs={"device": "cpu"}
)

# Chunker
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def deduplicate_chunks(chunks: list[Document]) -> list[Document]:
    seen = set()
    unique = []
    for doc in chunks:
        norm = doc.page_content.strip().lower()
        if norm in seen:
            continue
        seen.add(norm)
        unique.append(doc)
    return unique

def embed_all_txt_files():
    all_docs = []

    for txt_file in CLEAN_DIR.glob("*.txt"):
        text = txt_file.read_text(encoding="utf-8")
        chunks = splitter.create_documents([text], metadatas=[{"source": txt_file.name}])
        all_docs.extend(chunks)

    print(f"[i] Total chunks before dedup: {len(all_docs)}")

    unique_docs = deduplicate_chunks(all_docs)
    print(f"[✓] Unique chunks after dedup: {len(unique_docs)}")

    db = FAISS.from_documents(unique_docs, embedding_model)
    db.save_local(str(INDEX_DIR))
    print(f"[✓] Saved FAISS index to {INDEX_DIR}")

if __name__ == "__main__":
    embed_all_txt_files()
