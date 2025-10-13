import os
import fitz  # PyMuPDF for PDFs
from docx import Document
import pypandoc


def extract_text(file_path: str) -> tuple[str, list[str]]:
    """
    Extract text from a supported file and return both text and URLs.
    Supports: PDF, DOCX, ODT, TXT
    
    Returns:
        tuple: (text_content, list_of_urls)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text, urls = _extract_from_pdf(file_path)
    elif ext == ".docx":
        text, urls = _extract_from_docx(file_path)
    elif ext == ".odt":
        text = _extract_from_odt(file_path)
        urls = []
    elif ext == ".txt":
        text = _extract_from_txt(file_path)
        urls = []
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return text.strip(), urls


def _extract_from_pdf(file_path: str) -> tuple[str, list[str]]:
    """
    Extract text and embedded hyperlinks from PDF.
    """
    text = []
    urls = []
    
    with fitz.open(file_path) as doc:
        for page in doc:
            # Extract text
            page_text = page.get_text("text")
            text.append(page_text)
            
            # Extract hyperlinks
            for link in page.get_links():
                uri = link.get("uri", None)
                if uri and uri.startswith("http"):
                    urls.append(uri)
    
    return "\n".join(text).strip(), list(set(urls))


def _extract_from_docx(file_path: str) -> tuple[str, list[str]]:
    """
    Extract text and hyperlinks from DOCX.
    """
    doc = Document(file_path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    
    urls = []
    for rel in doc.part.rels.values():
        if "hyperlink" in rel.reltype and rel.target_ref:
            if rel.target_ref.startswith("http"):
                urls.append(rel.target_ref)
    
    return text.strip(), list(set(urls))


def _extract_from_odt(file_path: str) -> str:
    """Extract text from ODT files."""
    return pypandoc.convert_file(file_path, "plain", format="odt").strip()


def _extract_from_txt(file_path: str) -> str:
    """Extract text from plain text files."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()