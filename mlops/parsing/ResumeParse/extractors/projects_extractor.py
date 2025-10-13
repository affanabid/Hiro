import re
from typing import List, Dict


def extract_projects(text: str) -> List[Dict[str, str]]:
    """
    Extract project information from resume.
    Returns list of dicts with project name, tech stack, and description.
    """
    # Find projects section
    projects_section = extract_projects_section(text)
    
    if not projects_section:
        return []
    
    projects = []
    lines = projects_section.split('\n')
    
    current_project = None
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if current_project and current_project.get('name'):
                projects.append(current_project)
                current_project = None
            continue
        
        # Check if line is a project title (has tech stack in pipe format)
        tech_match = re.search(r'(.+?)\s*\|\s*(.+)', line)
        if tech_match and not line.startswith('•'):
            # This is likely a project header
            if current_project and current_project.get('name'):
                projects.append(current_project)
            
            current_project = {
                'name': tech_match.group(1).strip(),
                'technologies': tech_match.group(2).strip(),
                'description': ''
            }
        
        # Check if line is a bullet point (description)
        elif line.startswith('•') or line.startswith('-'):
            if current_project:
                desc = line.lstrip('•').lstrip('-').strip()
                if current_project['description']:
                    current_project['description'] += ' ' + desc
                else:
                    current_project['description'] = desc
        
        # Or if it's a continuation of description
        elif current_project and current_project.get('description'):
            current_project['description'] += ' ' + line
    
    # Add last project
    if current_project and current_project.get('name'):
        projects.append(current_project)
    
    # Clean up descriptions
    for project in projects:
        if project['description']:
            # Remove extra whitespace
            project['description'] = re.sub(r'\s+', ' ', project['description']).strip()
            # Limit length
            if len(project['description']) > 300:
                project['description'] = project['description'][:300] + '...'
    
    return projects


def extract_projects_section(text: str) -> str:
    """
    Extract the projects section from resume.
    """
    patterns = [
        r'Projects?[:\-]?\s*(.+?)(?=\n\s*(?:Experience|Education|Skills|Certifications|Technical Skills)[:\-]|\Z)',
        r'Academic\s+Projects?[:\-]?\s*(.+?)(?=\n\s*(?:Experience|Education|Skills|Certifications)[:\-]|\Z)',
        r'Personal\s+Projects?[:\-]?\s*(.+?)(?=\n\s*(?:Experience|Education|Skills|Certifications)[:\-]|\Z)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return ""


def format_projects_for_output(projects: List[Dict[str, str]]) -> List[str]:
    """
    Format projects as readable strings for JSON output.
    """
    formatted = []
    
    for project in projects:
        parts = [project['name']]
        
        if project.get('technologies'):
            parts.append(f"Tech: {project['technologies']}")
        
        if project.get('description'):
            parts.append(project['description'])
        
        formatted.append(' | '.join(parts))
    
    return formatted


# Test
if __name__ == "__main__":
    sample = """
    Projects
    Subjectify App | Python, Flask, BeautifulSoup, FASTAPI, GoogleAPIClient
    • Personalized Real Time Roadmap Development App.
    
    Breast Cancer Prediction App | Python, numpy, pandas, scikit-learn, Streamlit
    • Streamlit app using ML to classify diagnostic data.
    
    Student Portal Web App | Java Servlets, MySQL, Apache Tomcat
    • Complete CRUD based Web app with user auth and DB integration.
    """
    
    projects = extract_projects(sample)
    print("Extracted Projects:")
    for proj in projects:
        print(f"\n  Name: {proj['name']}")
        print(f"  Tech: {proj['technologies']}")
        print(f"  Desc: {proj['description']}")
    
    print("\n\nFormatted:")
    formatted = format_projects_for_output(projects)
    for p in formatted:
        print(f"  - {p}")