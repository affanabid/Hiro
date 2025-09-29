import os
import fitz  # PyMuPDF for PDFs
from docx import Document
import pypandoc

def extract_text(file_path: str) -> str:
    """
    Extract all text from a supported file.
    Supports: PDF, DOCX, ODT, TXT
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".docx":
        return _extract_from_docx(file_path)
    elif ext == ".odt":
        return _extract_from_odt(file_path)
    elif ext == ".txt":
        return _extract_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def _extract_from_pdf(file_path: str) -> str:
    text = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text.append(page.get_text("text"))
    return "\n".join(text).strip()

def _extract_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text).strip()

def _extract_from_odt(file_path: str) -> str:
    return pypandoc.convert_file(file_path, "plain", format="odt").strip()

def _extract_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


# Example usage:
file = "Suleman-Resume.pdf"   # or .docx, .odt, .txt
text = extract_text(file)

print(text)  # prteview first 1000 chars
