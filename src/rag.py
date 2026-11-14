
import ollama
from retrieval import retrieve_documents

client = ollama.Client(
    host="http://127.0.0.1:11434"
)



def generate_answer(question):

    results = retrieve_documents(question, top_k=3)

    retrieved_chunks = results["documents"][0]
    retrieved_sources = results["metadatas"][0]

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    You are a company policy assistant.

    Answer using ONLY the information in the context.
    If the answer is not present, say:
    "I don't have enough information to answer this."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = client.chat(
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.message.content,
        "retrieved_chunks": retrieved_chunks,
        "retrieved_sources": retrieved_sources
    }



if __name__ == "__main__":
    question = "How many annual leaves do employees get?"
    result = generate_answer(question)
    print(result["answer"])
