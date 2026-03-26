from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path("data/docs")

def load_pdfs():
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    documents = []

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        documents.append({
            "file_name": pdf_file.name,
            "text": text
        })

    return documents


def chunk_text(text: str, chunk_size: int = 500):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end

    return chunks


if __name__ == "__main__":
    docs = load_pdfs()

    if not docs:
        print("No PDF files found in data/docs/")
    else:
        for doc in docs:
            print(f"\nProcessing file: {doc['file_name']}")
            chunks = chunk_text(doc["text"])

            print(f"Total chunks: {len(chunks)}")

            for i, chunk in enumerate(chunks[:3], start=1):
                print(f"\nChunk {i}:")
                print(chunk[:300])