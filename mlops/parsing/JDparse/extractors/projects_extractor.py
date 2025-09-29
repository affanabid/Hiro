# jdparsing/extractors/projects_extractor.py
import re
from typing import List

PROJECT_VERBS = ["project", "experience building", "built", "developed", "designed", "worked on", "implemented"]

def extract_projects(text: str) -> List[str]:
    # naive: sentences that contain project verbs likely mention projects or domains
    sents = [s.strip() for s in text.split(".") if s.strip()]
    out = []
    low_text = text.lower()
    for s in sents:
        if any(verb in s.lower() for verb in PROJECT_VERBS):
            out.append(s.strip())
    return out
