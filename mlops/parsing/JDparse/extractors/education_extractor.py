# jdparsing/extractors/education_extractor.py
import re
from typing import List

DEGREE_PATTERNS = [
    r"(bachelor(?:'s)?(?: of)?(?: degree)?(?: in)?\s*[\w\s&+-]+)",
    r"(bsc(?:\.\s*)? in [\w\s&+-]+)",
    r"(ba(?:\.\s*)? in [\w\s&+-]+)",
    r"(master(?:'s)?(?: of)?(?: degree)?(?: in)?\s*[\w\s&+-]+)",
    r"(msc(?:\.\s*)? in [\w\s&+-]+)",
    r"(phd|doctorate)",
    r"(mba)",
    r"(degree in [\w\s&+-]+)"
]

def extract_education(text: str) -> List[str]:
    out = []
    low = text.lower()
    for patt in DEGREE_PATTERNS:
        for m in re.finditer(patt, text, flags=re.IGNORECASE):
            s = m.group(0).strip()
            out.append(s)
    # deduplicate
    return list(dict.fromkeys(out))
