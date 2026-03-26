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
            "text": text.strip()
        })

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def prepare_chunk_records():
    documents = load_pdfs()
    records = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for idx, chunk in enumerate(chunks, start=1):
            records.append({
                "file_name": doc["file_name"],
                "chunk_index": idx,
                "chunk_text": chunk
            })

    return records


if __name__ == "__main__":
    records = prepare_chunk_records()

    if not records:
        print("No PDF files found in data/docs/")
    else:
        print(f"Total chunk records: {len(records)}")

        for record in records[:5]:
            print("\n-------------------------")
            print(f"File Name   : {record['file_name']}")
            print(f"Chunk Index : {record['chunk_index']}")
            print(f"Chunk Text  : {record['chunk_text'][:300]}")