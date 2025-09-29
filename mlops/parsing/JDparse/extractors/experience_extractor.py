# jdparsing/extractors/experience_extractor.py
import re
from typing import Dict

LEVEL_KEYWORDS = {
    "entry": ["entry level", "junior", "jr."],
    "mid": ["mid-level", "mid level", "midlevel"],
    "senior": ["senior", "sr.", "lead", "manager"],
}

def extract_experience(text: str) -> Dict:
    """
    Return: {min_years: int|None, max_years: int|None, level: str|None, domains: List[str]}
    """
    res = {"min_years": None, "max_years": None, "level": None, "domains": []}

    # years patterns: "3+ years", "at least 5 years", "5-7 years", "minimum 4 years"
    patterns = [
        r"(\d+)\s*\+\s*years",
        r"at least\s*(\d+)\s*years",
        r"minimum\s*(\d+)\s*years",
        r"(\d+)\s*-\s*(\d+)\s*years",
        r"(\d+)\s*years"
    ]
    for patt in patterns:
        m = re.search(patt, text, flags=re.IGNORECASE)
        if m:
            if len(m.groups()) == 2:
                res["min_years"], res["max_years"] = int(m.group(1)), int(m.group(2))
            else:
                yrs = int(m.group(1))
                # If pattern had a trailing plus we consider that min only
                if "+" in patt or "at least" in patt or "minimum" in patt:
                    res["min_years"] = yrs
                else:
                    res["min_years"] = yrs
            break

    # level detection
    low = text.lower()
    for level, keys in LEVEL_KEYWORDS.items():
        for k in keys:
            if k in low:
                res["level"] = level
                break
        if res["level"]:
            break

    # domains: naive heuristics — common domains; you can extend list
    domain_vocab = ["backend", "frontend", "web development", "data science", "machine learning", "devops", "mobile", "qa", "security", "ai", "cloud"]
    for dom in domain_vocab:
        if dom in low:
            res["domains"].append(dom)

    return res
