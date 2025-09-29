# jdparsing/extractors/certifications_extractor.py
import re
from typing import List

CERT_PATTERNS = [
    r"(aws certified [\w\s]+)",
    r"(certified [\w\s]+)",
    r"(pmp)",
    r"(scrum master)",
    r"(gcp professional [\w\s]+)",
]

def extract_certifications(text: str) -> List[str]:
    out = []
    for patt in CERT_PATTERNS:
        for m in re.finditer(patt, text, flags=re.IGNORECASE):
            out.append(m.group(0).strip())
    return list(dict.fromkeys(out))
