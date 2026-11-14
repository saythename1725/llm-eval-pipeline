
from pathlib import Path
import ollama
import chromadb

from ingestion import load_documents

# Connect to Ollama
ollama_client = ollama.Client(
    host="http://127.0.0.1:11434"
)

# Create persistent ChromaDB database
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

# Create a collection
collection = chroma_client.get_or_create_collection(
    name="company_policies"
)


def store_documents():

    # Step 1: Load existing chunks
    chunks = load_documents()

    print("Total chunks loaded:", len(chunks))

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    # Step 2: Generate embeddings for each chunk
    for i, chunk in enumerate(chunks):

        result = ollama_client.embed(
            model="nomic-embed-text",
            input=chunk["text"]
        )

        documents.append(chunk["text"])
        embeddings.append(result.embeddings[0])

        metadatas.append({
            "source": chunk["source"]
        })

        ids.append(f"chunk_{i}")

    # Step 3: Store in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Successfully stored:", collection.count(), "chunks")


if __name__ == "__main__":
    store_documents()
