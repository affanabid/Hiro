# jdparsing/extractors/skills_extractor.py
from typing import List, Tuple
import spacy
from spacy.matcher import PhraseMatcher
from rapidfuzz import process, fuzz
import json
import os

nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger"])

# Load your canonical skills list from a file (one skill per line)
SKILLS_FILE = os.path.join(os.path.dirname(__file__), "skills_list.txt")

def load_skill_vocab(path=SKILLS_FILE) -> List[str]:
    if not os.path.exists(path):
        # create a tiny default list to get started
        default = ["python", "django", "flask", "react", "node.js", "aws", "docker", "kubernetes", "sql", "tensorflow", "pytorch", "machine learning"]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(default))
        return default
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

_skill_vocab = load_skill_vocab()
_phrase_matcher = None

def _build_phrase_matcher(vocab: List[str]):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(s) for s in sorted(set(vocab), key=len, reverse=True)]
    matcher.add("SKILL", patterns)
    return matcher

def extract_skills(text: str, top_k_fuzzy=3) -> Tuple[List[str], List[str]]:
    """
    Returns (hard_skills, soft_skills)
    Approach:
      1. PhraseMatcher against canonical vocabulary (hard skills).
      2. Fallback fuzzy match for tokens if phrase matcher misses them.
      3. Soft skills detection via small heuristics list.
    """
    global _phrase_matcher, _skill_vocab
    if _phrase_matcher is None:
        _phrase_matcher = _build_phrase_matcher(_skill_vocab)

    doc = nlp(text)
    matches = _phrase_matcher(doc)
    hard = set()
    for match_id, start, end in matches:
        span = doc[start:end].text.strip()
        hard.add(span)

    # fuzzy search on tokens (to catch slight variations)
    tokens = [t.text for t in doc if not t.is_stop and not t.is_punct and len(t.text) > 1]
    for tok in tokens:
        best = process.extractOne(tok, _skill_vocab, scorer=fuzz.WRatio)
        if best and best[1] >= 85:  # threshold; tune later
            hard.add(best[0])

    # soft skills: small rule-based list
    soft_vocab = ["communication", "teamwork", "leadership", "problem solving", "collaboration", "adaptability", "time management"]
    soft = [s for s in soft_vocab if s in text.lower()]

    return sorted(hard), sorted(soft)
