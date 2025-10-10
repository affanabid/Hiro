import re
from datetime import datetime
from typing import List, Dict


def extract_experience(text: str) -> str:
    """
    Calculate total years of experience from work history.
    Returns string like '2 years' or '6 months' or '1.5 years'
    """
    # Find experience section
    exp_section = extract_experience_section(text)
    
    if not exp_section:
        # Fallback: search for explicit experience mentions
        explicit = find_explicit_experience(text)
        if explicit:
            return explicit
        return "0 years"
    
    # Extract all date ranges
    date_ranges = extract_date_ranges(exp_section)
    
    if not date_ranges:
        return "0 years"
    
    # Calculate total months
    total_months = 0
    for start, end in date_ranges:
        months = calculate_months_between(start, end)
        total_months += months
    
    # Convert to years/months
    if total_months == 0:
        return "0 years"
    elif total_months < 12:
        return f"{total_months} months"
    else:
        years = total_months // 12
        remaining_months = total_months % 12
        if remaining_months >= 6:
            return f"{years + 0.5} years"
        else:
            return f"{years} years"


def extract_experience_section(text: str) -> str:
    """
    Extract the experience/work history section.
    """
    patterns = [
        r'(?:Work\s+)?Experience[:\-]?\s*(.+?)(?=\n\s*(?:Education|Projects|Skills|Certifications)[:\-]|\Z)',
        r'(?:Professional\s+)?(?:Work\s+)?History[:\-]?\s*(.+?)(?=\n\s*(?:Education|Projects|Skills|Certifications)[:\-]|\Z)',
        r'Employment[:\-]?\s*(.+?)(?=\n\s*(?:Education|Projects|Skills|Certifications)[:\-]|\Z)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return ""


def find_explicit_experience(text: str) -> str:
    """
    Find explicitly stated experience like '5+ years of experience'
    """
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'(?:experience|exp)(?:\s+of)?\s+(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if match.lastindex == 2:
                # Range like "3-5 years"
                return f"{match.group(1)}-{match.group(2)} years"
            else:
                return f"{match.group(1)} years"
    
    return ""


def extract_date_ranges(text: str) -> List[tuple]:
    """
    Extract date ranges from experience section.
    Returns list of (start_date, end_date) tuples as datetime objects.
    """
    date_ranges = []
    
    # Pattern for date ranges like "June 2024 – Jan 2025" or "May 2024 – Aug 2024"
    pattern = r'([A-Z][a-z]+\.?\s+\d{4})\s*[-–—]\s*([A-Z][a-z]+\.?\s+\d{4}|Present|Current)'
    
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    for start_str, end_str in matches:
        try:
            # Parse start date
            start_date = parse_date(start_str)
            
            # Parse end date (or use current date if "Present")
            if end_str.lower() in ['present', 'current']:
                end_date = datetime.now()
            else:
                end_date = parse_date(end_str)
            
            date_ranges.append((start_date, end_date))
        except:
            continue
    
    return date_ranges


def parse_date(date_str: str) -> datetime:
    """
    Parse date string like 'June 2024' or 'Jun. 2024' to datetime.
    """
    date_str = date_str.strip().replace('.', '')
    
    # Try different formats
    formats = [
        "%B %Y",  # June 2024
        "%b %Y",  # Jun 2024
        "%m/%Y",  # 06/2024
        "%Y",     # 2024
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    raise ValueError(f"Could not parse date: {date_str}")


def calculate_months_between(start: datetime, end: datetime) -> int:
    """
    Calculate number of months between two dates.
    """
    years_diff = end.year - start.year
    months_diff = end.month - start.month
    total_months = years_diff * 12 + months_diff
    
    return max(0, total_months)


def extract_companies(text: str) -> List[str]:
    """
    Extract company names from experience section.
    """
    exp_section = extract_experience_section(text)
    if not exp_section:
        return []
    
    companies = []
    
    # Look for company names (usually follow job titles)
    # Pattern: Job Title followed by dates, then company name
    lines = exp_section.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines and dates
        if not line or re.match(r'^[A-Z][a-z]+\.?\s+\d{4}\s*[-–]', line):
            continue
        
        # Check if line looks like a company name
        # Usually capitalized, not too long, not a bullet point
        if (line[0].isupper() and 
            len(line.split()) <= 6 and 
            not line.startswith('•') and
            not re.match(r'^[A-Z][a-z]+\s+\d{4}', line)):
            
            # Additional validation: not a location or common header
            if not any(word in line.lower() for word in [
                'remote', 'experience', 'responsibilities', 'achievements'
            ]):
                companies.append(line)
    
    return list(dict.fromkeys(companies))  # Remove duplicates


# Test
if __name__ == "__main__":
    sample = """
    Experience
    Crypto Data Analyst
    June 2024 – Jan 2025
    DATXOC
    Remote
    • Analyzed historical and live crypto trading data
    
    Artificial Intelligence Intern
    May 2024 – Aug 2024
    DataVerse Labs
    Lahore
    • Assisted in building a movie recommendation system
    """
    
    years = extract_experience(sample)
    print(f"Total Experience: {years}")
    
    companies = extract_companies(sample)
    print(f"Companies: {companies}")