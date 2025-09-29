# jdparsing/segmentation.py
import re
from typing import Dict

SECTION_HEADERS = [
    r"responsibilities",
    r"requirements",
    r"qualifications",
    r"skills",
    r"about the role",
    r"what we're looking for",
    r"preferred",
    r"education",
    r"experience",
]

import re

def extract_title(jd_text: str) -> str:
    # Try to match 'Job Title:' pattern
    match = re.search(r'Job Title:\s*(.+)', jd_text, re.IGNORECASE)
    if match:
        # Stop at the first line break after title
        title_line = match.group(1).split("\n")[0]
        return title_line.strip()
    
    # Fallback: first line only
    return jd_text.strip().split("\n")[0]

def split_sections(text: str) -> Dict[str, str]:
    """
    Very pragmatic approach: look for known headers and cut text accordingly.
    Returns a dict with keys: title, requirements, responsibilities, qualifications, others.
    """
    sections = {}
    lowered = text.lower()
    # try to extract title as first line / header if short
    # first_line = text.splitlines()[0].strip()
    # sections['title'] = first_line if len(first_line.split()) <= 8 else None
    sections['title'] = extract_title(text)

    # naive splitting
    pattern = "(" + "|".join(SECTION_HEADERS) + r")[:\s\-]*"
    # find header positions
    headers = list(re.finditer(pattern, lowered, flags=re.IGNORECASE))
    if not headers:
        sections['body'] = text
        return sections

    # build mapping header -> text until next header
    for i, m in enumerate(headers):
        h = m.group(0).strip()
        start = m.start()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        header_name = re.sub(r"[:\s\-]*$", "", h, flags=re.IGNORECASE)
        sections[header_name] = text[start:end].strip()

    return sections
