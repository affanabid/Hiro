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
    Job Title: Backend Engineer (Python/Django)

    We are looking for a Backend Engineer to join our team and help build scalable APIs and data-driven applications.

    Responsibilities:
    - Design, develop, and maintain backend services using Python and Django
    - Work with relational databases (PostgreSQL, MySQL) and write optimized SQL queries
    - Build RESTful and GraphQL APIs to power web and mobile applications
    - Collaborate with front-end developers, DevOps, and product managers to deliver high-quality features
    - Implement authentication, authorization, and security best practices
    - Optimize application performance and handle large-scale traffic

    Requirements:
    - Bachelor's or Master's degree in Computer Science, Software Engineering, or related field
    - 3-9 years of professional experience in backend development
    - Strong proficiency in Python and Django
    - Experience with containerization (Docker, Kubernetes) and cloud platforms (AWS/GCP/Azure)
    - Solid understanding of CI/CD pipelines and version control (Git)
    - Hands-on experience with caching (Redis, Memcached) and message brokers (RabbitMQ, Kafka)
    - Knowledge of software design patterns, data structures, and algorithms
    - Familiarity with microservices architecture

    Preferred Qualifications:
    - Experience with machine learning model deployment
    - Open-source contributions or personal projects on GitHub
    - Certifications in cloud computing or DevOps tools

    """
    parsed = parse_job_description(sample)
    # print(parsed.json(indent=2))
    print(parsed.model_dump_json(indent=2))
