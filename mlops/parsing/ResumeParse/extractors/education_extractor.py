import re
from typing import List


def extract_education(text: str) -> List[dict]:
    """
    Extract education entries with degree, institution, location, and dates.
    Returns list of structured education dicts.
    """
    # Split text into sections
    sections = re.split(r'\n\s*\n', text)
    
    education_entries = []
    
    # Common degree patterns
    degree_patterns = [
        r'\b(?:BS|BSc|B\.S\.|Bachelor(?:\'s)?)\s+(?:of\s+)?(?:Science\s+)?(?:in\s+)?([A-Za-z\s&]+?)(?=\s*\n|\s*Expected|\s*\d{4}|\s*[A-Z][a-z]+\s+\d{4})',
        r'\b(?:MS|MSc|M\.S\.|Master(?:\'s)?)\s+(?:of\s+)?(?:Science\s+)?(?:in\s+)?([A-Za-z\s&]+?)(?=\s*\n|\s*Expected|\s*\d{4})',
        r'\b(?:PhD|Ph\.D\.|Doctorate)\s+(?:in\s+)?([A-Za-z\s&]+?)(?=\s*\n|\s*Expected|\s*\d{4})',
        r'\b(?:MBA|BBA|MPhil)\b',
        r'\b(?:Intermediate|Matriculation|O-Level|A-Level)\b',
    ]
    
    # Look for education section
    edu_section_idx = -1
    for i, section in enumerate(sections):
        if re.search(r'^\s*Education\s*$', section, re.IGNORECASE | re.MULTILINE):
            edu_section_idx = i
            break
    
    # If education section found, focus on that and next few sections
    if edu_section_idx >= 0:
        relevant_text = '\n\n'.join(sections[edu_section_idx:edu_section_idx+5])
    else:
        relevant_text = text
    
    # Split by newlines and process
    lines = relevant_text.split('\n')
    
    current_entry = {}
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            if current_entry:
                education_entries.append(current_entry)
                current_entry = {}
            continue
        
        # Skip "Education" header
        if re.match(r'^\s*Education\s*$', line, re.IGNORECASE):
            continue
        
        # Check for degree
        degree_found = False
        for pattern in degree_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                if not current_entry:
                    current_entry = {'degree': '', 'field': '', 'institution': '', 'location': '', 'dates': ''}
                
                degree_text = match.group(0)
                if match.groups():
                    current_entry['degree'] = degree_text.split(match.group(1))[0].strip()
                    current_entry['field'] = match.group(1).strip()
                else:
                    current_entry['degree'] = degree_text
                
                degree_found = True
                break
        
        if degree_found:
            continue
        
        # Check for dates (graduation date or range)
        date_match = re.search(r'(?:Expected\s+)?([A-Z][a-z]+\s+\d{4}|\d{4}|[A-Z][a-z]+\.\s+\d{4}\s*[-–]\s*[A-Z][a-z]+\.\s+\d{4})', line)
        if date_match and current_entry:
            current_entry['dates'] = date_match.group(1).strip()
            continue
        
        # Check if line is institution (usually capitalized, longer text)
        if current_entry and not current_entry.get('institution'):
            # University/College/Institute indicators
            if any(keyword in line for keyword in ['University', 'College', 'Institute', 'School', 'Academy']):
                current_entry['institution'] = line
                continue
            # Or if it's a capitalized line after degree
            elif len(line.split()) >= 2 and line[0].isupper():
                current_entry['institution'] = line
                continue
        
        # Check for location (city names, usually shorter)
        if current_entry and not current_entry.get('location') and current_entry.get('institution'):
            if len(line.split()) <= 3 and line[0].isupper():
                current_entry['location'] = line
    
    # Add last entry
    if current_entry:
        education_entries.append(current_entry)
    
    # Format entries as strings
    formatted_entries = []
    for entry in education_entries:
        parts = []
        
        if entry.get('degree'):
            if entry.get('field'):
                parts.append(f"{entry['degree']} in {entry['field']}")
            else:
                parts.append(entry['degree'])
        
        if entry.get('institution'):
            parts.append(entry['institution'])
        
        if entry.get('location'):
            parts.append(entry['location'])
        
        if entry.get('dates'):
            parts.append(f"({entry['dates']})")
        
        if parts:
            formatted_entries.append(' - '.join(parts))
    
    # Remove duplicates and return
    return list(dict.fromkeys(formatted_entries))


# Test
if __name__ == "__main__":
    sample = """
    Education
    Punjab University College of Information and Technology (PUCIT)
    Lahore
    BS Data Science
    Expected June 2026
    Government College University (GCU)
    Lahore
    Intermediate
    Aug. 2019 – Sep 2021
    """
    
    result = extract_education(sample)
    for edu in result:
        print(edu)