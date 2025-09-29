# jdparsing/preprocessing.py
import re
import html
from typing import List
import spacy

nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])

def clean_text(raw: str) -> str:
    """Basic cleaning: strip HTML, unescape entities, normalize whitespace."""
    if not raw:
        return ""
    text = html.unescape(raw)
    # remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # normalize unicode spaces, replace multiple whitespace with single space
    text = re.sub(r"\s+", " ", text).strip()
    return text

def sentence_tokenize(text: str) -> List[str]:
    """Split into sentences using spaCy's sentencizer for robustness."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]
