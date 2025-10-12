import re
from typing import List, Set


# Comprehensive skill database organized by category
SKILL_DATABASE = {
    # Programming Languages
    "languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Shell",
        "Bash", "PowerShell", "SQL", "HTML", "CSS", "Dart", "Objective-C"
    ],
    
    # Frameworks & Libraries
    "frameworks": [
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", 
        "FastAPI", "Spring", "Spring Boot", ".NET", "ASP.NET", "Laravel", "Rails",
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy",
        "Matplotlib", "Seaborn", "Plotly", "D3.js", "jQuery", "Bootstrap", "Tailwind"
    ],
    
    # Databases
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQL Server", "SQLite",
        "Redis", "Cassandra", "DynamoDB", "Firebase", "Elasticsearch", "MariaDB"
    ],
    
    # Cloud & DevOps
    "cloud": [
        "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins",
        "CI/CD", "Terraform", "Ansible", "Git", "GitHub", "GitLab", "Bitbucket",
        "Linux", "Unix", "Nginx", "Apache"
    ],
    
    # Data & Analytics
    "data": [
        "Power BI", "Tableau", "Excel", "Data Science", "Machine Learning",
        "Deep Learning", "NLP", "Computer Vision", "Data Analysis", "Statistics",
        "Big Data", "Hadoop", "Spark", "ETL", "Data Warehousing", "Data Mining",
        "Data Visualization", "Business Intelligence"
    ],
    
    # Tools & Others
    "tools": [
        "VS Code", "Visual Studio", "IntelliJ", "Eclipse", "PyCharm", "Jupyter",
        "Postman", "JIRA", "Confluence", "Slack", "Trello", "Figma", "Sketch",
        "Photoshop", "Illustrator", "Microsoft Office", "Google Workspace"
    ],
    
    # Methodologies
    "methodologies": [
        "Agile", "Scrum", "Kanban", "DevOps", "TDD", "BDD", "REST API", "GraphQL",
        "Microservices", "Serverless", "Object-Oriented Programming", "OOP",
        "Functional Programming", "Design Patterns"
    ],
    
    # Soft Skills
    "soft": [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management", "Project Management",
        "Public Speaking", "Presentation", "Research", "Analytical Skills"
    ]
}

# Flatten all skills into one list
ALL_SKILLS = []
for category in SKILL_DATABASE.values():
    ALL_SKILLS.extend(category)


def extract_skills(text: str) -> List[str]:
    """
    Extract technical and soft skills from resume text.
    Uses exact matching, case-insensitive with word boundaries.
    """
    found_skills: Set[str] = set()
    text_lower = text.lower()
    
    # Find technical/skills section
    skills_section = extract_skills_section(text)
    
    # If we found a skills section, prioritize it
    search_text = skills_section if skills_section else text
    search_text_lower = search_text.lower()
    
    # Method 1: Exact match with word boundaries
    for skill in ALL_SKILLS:
        # Create pattern with word boundaries
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, search_text_lower):
            found_skills.add(skill)
    
    # Method 2: Parse skills section if exists
    if skills_section:
        # Split by common delimiters
        tokens = re.split(r'[,;\n•\-\|]', skills_section)
        for token in tokens:
            token = token.strip()
            # Skip empty or very short tokens
            if len(token) < 2 or len(token) > 50:
                continue
            
            # Skip common section headers
            if any(header in token.lower() for header in [
                'skills:', 'technical skills', 'languages:', 'frameworks:',
                'tools:', 'databases:', 'soft skills'
            ]):
                continue
            
            # Check if token is a known skill
            token_lower = token.lower()
            for skill in ALL_SKILLS:
                if token_lower == skill.lower() or token_lower in skill.lower():
                    found_skills.add(skill)
                    break
            else:
                # If not in database but looks like a skill (capitalized, reasonable length)
                if token[0].isupper() and 3 <= len(token) <= 30:
                    # Additional validation: not a common word
                    if not any(word in token.lower() for word in [
                        'experience', 'education', 'project', 'worked', 'developed',
                        'university', 'college', 'company', 'team', 'using'
                    ]):
                        found_skills.add(token.title())
    
    # Sort skills for consistent output
    return sorted(found_skills)


def extract_skills_section(text: str) -> str:
    """
    Extract the skills section from resume if it exists.
    """
    # Look for skills section headers
    patterns = [
        r'(?:Technical\s+)?Skills[:\-]?\s*(.+?)(?=\n\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*[:\-]|\n\s*\n|$)',
        r'(?:Core\s+)?Competencies[:\-]?\s*(.+?)(?=\n\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*[:\-]|\n\s*\n|$)',
        r'Technologies[:\-]?\s*(.+?)(?=\n\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*[:\-]|\n\s*\n|$)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return ""


# Test
if __name__ == "__main__":
    sample = """
    Technical Skills
    Languages: Python, Java, C/C++, SQL (MySQL), JavaScript, HTML/CSS, MATLAB
    Frameworks: Flask, FastAPI, Scikit-learn
    Developer Tools: Git, Docker, Google Cloud Platform, VS Code, Visual Studio
    Libraries: Pandas, Numpy, BeautifulSoup, Selenium, Streamlit, Matplotlib, Seaborn
    """
    
    skills = extract_skills(sample)
    print("Extracted Skills:")
    for skill in skills:
        print(f"  - {skill}")