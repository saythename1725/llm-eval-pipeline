
import ollama
import numpy as np

client = ollama.Client(host="http://127.0.0.1:11434")

text1 = "Every full-time employee receives 20 paid leaves annually."

text2 = "Employees get 20 annual vacation days."

text3 = "The company provides reimbursement up to Rs. 5000."

# Generate embeddings
result = client.embed(
    model="nomic-embed-text",
    input=[text1, text2, text3]
)

embeddings = result.embeddings

print("Number of embeddings:", len(embeddings))
print("Dimensions:", len(embeddings[0]))


# Calculate cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


print("\nSimilarity between sentence 1 and 2:",
      cosine_similarity(embeddings[0], embeddings[1]))

print("Similarity between sentence 1 and 3:",
      cosine_similarity(embeddings[0], embeddings[2]))
