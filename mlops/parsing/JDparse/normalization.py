# jdparsing/normalization.py
from rapidfuzz import process, fuzz
from typing import List
import re

# A small mapping for degree normalization; extend as needed
DEGREE_MAP = {
    "bsc": "Bachelor's Degree",
    "bachelor": "Bachelor's Degree",
    "ba": "Bachelor's Degree",
    "msc": "Master's Degree",
    "master": "Master's Degree",
    "phd": "PhD",
    "mba": "MBA",
}

def normalize_skill(skill: str, skill_vocab: List[str]) -> str:
    """Fuzzy map skill to canonical vocab. If no good match, return original lowercased."""
    best = process.extractOne(skill, skill_vocab, scorer=fuzz.WRatio)
    if best and best[1] >= 80:
        return best[0]
    return skill.lower()

def normalize_education(items: List[str]) -> List[str]:
    out = []
    for s in items:
        low = s.lower()
        # try to find key words
        for k, v in DEGREE_MAP.items():
            if k in low:
                out.append(v)
                break
        else:
            # fallback clean up
            out.append(re.sub(r"\s+", " ", s).strip())
    return list(dict.fromkeys(out))
