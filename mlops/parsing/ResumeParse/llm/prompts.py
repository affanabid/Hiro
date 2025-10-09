def resume_extraction_prompt(resume_text: str) -> str:
    """
    Create a detailed prompt for LLM to extract structured resume data.
    """
    return f"""You are a precise resume parser. Extract structured information from the resume below.

CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON, no markdown, no explanations
2. Extract exact information from the resume - do not invent data
3. For arrays, return empty [] if no data found
4. For strings, return empty "" if no data found
5. Be precise with names, emails, and dates

OUTPUT SCHEMA:
{{
  "name": "Full name of candidate",
  "email": "Primary email address",
  "phone": "Primary phone number",
  "linkedin": "LinkedIn profile URL if present",
  "github": "GitHub profile URL if present",
  "education": [
    {{
      "degree": "Degree type (BS, MS, PhD, etc.)",
      "field": "Field of study",
      "institution": "University/College name",
      "location": "City/Location",
      "graduation_date": "Expected June 2026 or year"
    }}
  ],
  "skills": ["skill1", "skill2", "skill3"],
  "experience": [
    {{
      "title": "Job title",
      "company": "Company name",
      "location": "Location (City or Remote)",
      "start_date": "Start date",
      "end_date": "End date or Present",
      "responsibilities": ["responsibility 1", "responsibility 2"]
    }}
  ],
  "projects": [
    {{
      "name": "Project name",
      "technologies": "Tech stack",
      "description": "Brief description"
    }}
  ],
  "certifications": ["Certification 1", "Certification 2"],
  "summary": "Brief professional summary if present in resume"
}}

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

Return only the JSON object, nothing else."""


def resume_extraction_prompt_simple(resume_text: str) -> str:
    """
    Simplified prompt for faster extraction with basic schema.
    """
    return f"""Extract resume information as JSON only. No explanations.

JSON Schema:
{{
  "name": "",
  "email": "",
  "phone": "",
  "linkedin": "",
  "github": "",
  "education": [],
  "skills": [],
  "experience_years": "",
  "companies": [],
  "projects": [],
  "certifications": [],
  "summary": ""
}}

Resume:
{resume_text}

JSON only:"""