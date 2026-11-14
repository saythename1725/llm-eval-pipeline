
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Locate the documents folder
DOCUMENTS_PATH = Path(__file__).resolve().parent.parent / "documents"

# Configure our chunking strategy
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

def load_documents():
    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        chunks = splitter.split_text(text)

        for chunk in chunks:
            documents.append({
                "text": chunk,
                "source": file_path.name
            })

    return documents


if __name__ == "__main__":
    chunks = load_documents()

    print("Total chunks:", len(chunks))


    for i, chunk in enumerate(chunks):

        print("\n" + "=" * 60)
        print(f"CHUNK NUMBER: {i + 1}")
        print(f"SOURCE FILE: {chunk['source']}")
        print(f"CHARACTER COUNT: {len(chunk['text'])}")
        print("-" * 60)
        print(chunk["text"])

