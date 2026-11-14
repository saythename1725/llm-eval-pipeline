
import ollama
import chromadb

from pathlib import Path

# Connect to Ollama
ollama_client = ollama.Client(
    host="http://127.0.0.1:11434"
)

# Connect to existing ChromaDB
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = chroma_client.get_collection(
    name="company_policies"
)


def retrieve_documents(query, top_k=3):

    # Step 1: Convert user question into embedding
    result = ollama_client.embed(
        model="nomic-embed-text",
        input=query
    )

    query_embedding = result.embeddings[0]

    # Step 2: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = "Can I work from home during probation?"

    results = retrieve_documents(question)

    print("\nUSER QUESTION:", question)

    for i, document in enumerate(results["documents"][0]):

        print("\n" + "=" * 50)
        print("RESULT:", i + 1)
        print("DOCUMENT:", document)
        print("SOURCE:", results["metadatas"][0][i])
        print("DISTANCE:", results["distances"][0][i])
