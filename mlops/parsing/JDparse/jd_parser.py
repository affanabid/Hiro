# jdparsing/jd_parser.py
from .schema import FunctionalJD, Experience
from .preprocessing import clean_text, sentence_tokenize
from .segmentation import split_sections
from .extractors.skills_extractor import extract_skills, load_skill_vocab
from .extractors.experience_extractor import extract_experience
from .extractors.education_extractor import extract_education
from .extractors.projects_extractor import extract_projects
from .extractors.certifications_extractor import extract_certifications
from .normalization import normalize_skill, normalize_education

from .llm.client import call_llm
from .llm.prompts import jd_extraction_prompt
import json

def parse_job_description(jd_text: str) -> FunctionalJD:
    """
    Parses JD using LLM for structured field extraction.
    """
    # 1. Create prompt
    prompt = jd_extraction_prompt(jd_text)

    # 2. Call LLM
    llm_response = call_llm(prompt)

    # 3. Load JSON from LLM response
    try:
        jd_data = json.loads(llm_response)
    except json.JSONDecodeError:
        print("LLM returned invalid JSON, using empty schema.")
        jd_data = {}

    # ✅ Extract projects first using rule-based method
    projects = extract_projects(jd_text)
    if not projects:
        # fallback to LLM parsed projects
        projects = jd_data.get("projects", [])

    # 4. Map LLM output to schema with defaults
    parsed = FunctionalJD(
        title = jd_data.get("title"),
        skills_hard = jd_data.get("skills_hard", []),
        skills_soft = jd_data.get("skills_soft", []),
        experience = {
            "min_years": jd_data.get("experience_min_years"),
            "max_years": jd_data.get("experience_max_years"),
            "level": None,
            "domains": []
        },
        education = jd_data.get("education", []),
        certifications = jd_data.get("certifications", []),
        projects = jd_data.get("projects", []),
        other_requirements = jd_data.get("other_requirements", [])
    )
    return parsed

if __name__ == "__main__":
    sample = """
    Data Scientist - Remote
    We are hiring a Data Scientist to help us build data-driven products and insights.
    Key responsibilities:
    - Develop and deploy machine learning models for prediction and classification
    - Analyze large datasets using Python, Pandas, and SQL
    - Communicate insights effectively to stakeholders
    Required skills:
    - 3+ years of experience as a Data Scientist or ML Engineer
    - Strong knowledge of statistics, Python, scikit-learn, and visualization tools (Matplotlib, Seaborn, Power BI)
    - Experience working with cloud platforms (AWS or GCP)
    Preferred qualifications:
    - Master's or Ph.D. in Computer Science, Data Science, or related field
    - Experience with deep learning frameworks like TensorFlow or PyTorch
    """
    parsed = parse_job_description(sample)
    # print(parsed.json(indent=2))
    print(parsed.model_dump_json(indent=2))
