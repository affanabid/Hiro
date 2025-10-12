# jdparsing/extractors/projects_extractor.py
import re
from typing import List

PROJECT_KEYWORDS = [
    r"\bproject(s)?\b",
    r"open[-\s]?source",
    r"personal project(s)?",
    r"side project(s)?",
    r"github",
    r"contribution(s)?",
    r"develop(ed|ing)?",
    r"built",
    r"implemented",
    r"experience with",
    r"experience in",
    r"experience (building|developing)"
]

PROJECT_PATTERN = re.compile("|".join(PROJECT_KEYWORDS), flags=re.IGNORECASE)

def extract_projects(text: str) -> List[str]:
    """
    Extracts project-related phrases or sentences from job descriptions
    using keyword patterns.
    """
    # Split text into lines to catch bullet points and qualifications
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    projects = []

    for line in lines:
        if PROJECT_PATTERN.search(line):
            # Clean up line: remove leading dashes/bullets
            cleaned = re.sub(r"^[\-\*\•\s]+", "", line).strip()
            projects.append(cleaned)

    # Deduplicate while preserving order
    seen = set()
    unique_projects = []
    for p in projects:
        if p not in seen:
            unique_projects.append(p)
            seen.add(p)

    return unique_projects
