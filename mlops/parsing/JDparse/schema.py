# jdparsing/schema.py
from typing import List, Optional
from pydantic import BaseModel

class Experience(BaseModel):
    min_years: Optional[int] = None
    max_years: Optional[int] = None
    level: Optional[str] = None     # "entry", "mid", "senior", etc.
    domains: List[str] = []

class FunctionalJD(BaseModel):
    title: Optional[str] = None
    skills_hard: List[str] = []
    skills_soft: List[str] = []
    experience: Experience = Experience()
    education: List[str] = []
    certifications: List[str] = []
    projects: List[str] = []
    other_requirements: List[str] = []
