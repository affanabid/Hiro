def jd_extraction_prompt(jd_text: str) -> str:
    return f"""
Extract structured information from the following job description. 
STRICTLY RETURN ONLY A VALID JSON OBJECT. DO NOT WRITE ANY EXPLANATION OR EXTRA TEXT.

Job Description:
{jd_text}

JSON format:
{{
  "title": "<Job Title>",
  "skills_hard": ["<hard skill 1>", "<hard skill 2>"],
  "skills_soft": ["<soft skill 1>", "<soft skill 2>"],
  "experience_min_years": <minimum years of experience, integer>,
  "experience_max_years": <maximum years of experience, integer>,
  "education": ["<degree 1>", "<degree 2>"],
  "projects": ["<project 1>", "<project 2>"],
  "certifications": ["<certification 1>", "<certification 2>"],
  "other_requirements": ["<other requirement 1>", "<other requirement 2>"]
}}
"""
