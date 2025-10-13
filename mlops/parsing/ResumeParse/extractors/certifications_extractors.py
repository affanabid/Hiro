import re
from typing import List


# Common certification providers and keywords
CERT_PROVIDERS = [
    "AWS", "Amazon", "Microsoft", "Azure", "Google", "GCP", "Oracle", "IBM",
    "Cisco", "CompTIA", "Red Hat", "VMware", "Salesforce", "SAP", "PMI",
    "Scrum.org", "Scrum Alliance", "ISACA", "ISC2", "(ISC)²", "EC-Council",
    "Linux Foundation", "Python Institute", "Java", "Coursera", "edX",
    "Udacity", "DataCamp", "Kaggle", "HackerRank"
]

CERT_KEYWORDS = [
    "Certified", "Certification", "Certificate", "Professional", "Associate",
    "Expert", "Specialist", "Developer", "Architect", "Administrator",
    "Engineer", "Practitioner", "Master", "Advanced"
]

CERT_TYPES = [
    "AWS Certified", "Azure Certified", "Google Certified", "Microsoft Certified",
    "Cisco Certified", "CompTIA", "PMP", "CAPM", "CSM", "CSPO", "PSM",
    "ITIL", "Six Sigma", "Lean", "CEH", "CISSP", "Security+", "Network+",
    "A+", "Cloud+", "Linux+", "CCNA", "CCNP", "MCSA", "MCSE", "OCA", "OCP"
]


def extract_certifications(text: str) -> List[str]:
    """
    Extract professional certifications from resume text.
    Returns list of certification names with issuing organization if available.
    """
    # Find certifications section
    cert_section = extract_certifications_section(text)
    
    # If no section found, search in full text
    search_text = cert_section if cert_section else text
    
    certifications = set()
    
    # Method 1: Look for known certification types
    for cert_type in CERT_TYPES:
        pattern = r'\b' + re.escape(cert_type) + r'\b.*?(?=\n|$)'
        matches = re.findall(pattern, search_text, re.IGNORECASE)
        for match in matches:
            # Clean up the match
            cleaned = clean_certification_text(match)
            if cleaned:
                certifications.add(cleaned)
    
    # Method 2: Look for certification patterns
    patterns = [
        # "Certified [Something] by [Provider]"
        r'Certified\s+[\w\s]+(?:by|from)\s+[A-Z][\w\s]+',
        # "[Provider] Certified [Something]"
        r'(?:' + '|'.join(re.escape(p) for p in CERT_PROVIDERS) + r')\s+Certified\s+[\w\s]+',
        # "Certificate in [Something]"
        r'Certificate\s+(?:in|of)\s+[\w\s]+',
        # "[Something] Certification"
        r'[\w\s]+\s+Certification(?:\s+by|\s+from)?\s*[A-Z][\w\s]*'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, search_text, re.IGNORECASE)
        for match in matches:
            cleaned = clean_certification_text(match)
            if cleaned and is_valid_certification(cleaned):
                certifications.add(cleaned)
    
    # Method 3: Parse certifications section line by line if it exists
    if cert_section:
        lines = cert_section.split('\n')
        for line in lines:
            line = line.strip().lstrip('•').lstrip('-').strip()
            
            # Skip section headers and empty lines
            if (not line or 
                line.lower() in ['certifications', 'certificates', 'professional certifications']):
                continue
            
            # Check if line contains certification indicators
            if (any(keyword in line for keyword in CERT_KEYWORDS) or
                any(provider in line for provider in CERT_PROVIDERS)):
                
                cleaned = clean_certification_text(line)
                if cleaned and is_valid_certification(cleaned):
                    certifications.add(cleaned)
    
    # Remove false positives and sort
    valid_certs = [cert for cert in certifications if is_valid_certification(cert)]
    return sorted(valid_certs)


def extract_certifications_section(text: str) -> str:
    """
    Extract the certifications section from resume.
    """
    patterns = [
        r'Certifications?[:\-]?\s*(.+?)(?=\n\s*(?:Experience|Education|Skills|Projects|References)[:\-]|\Z)',
        r'Professional\s+Certifications?[:\-]?\s*(.+?)(?=\n\s*(?:Experience|Education|Skills|Projects)[:\-]|\Z)',
        r'Licenses?\s+(?:and|&)\s+Certifications?[:\-]?\s*(.+?)(?=\n\s*(?:Experience|Education|Skills|Projects)[:\-]|\Z)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return ""


def clean_certification_text(text: str) -> str:
    """
    Clean and format certification text.
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove dates in parentheses
    text = re.sub(r'\s*\([^)]*\d{4}[^)]*\)', '', text)
    
    # Remove trailing punctuation
    text = text.rstrip('.,;:')
    
    # Limit length
    if len(text) > 100:
        text = text[:100]
    
    return text.strip()


def is_valid_certification(cert: str) -> bool:
    """
    Validate if the extracted text is likely a real certification.
    """
    # Minimum length check
    if len(cert) < 5:
        return False
    
    # Must contain at least one certification keyword or provider
    has_keyword = any(keyword.lower() in cert.lower() for keyword in CERT_KEYWORDS)
    has_provider = any(provider.lower() in cert.lower() for provider in CERT_PROVIDERS)
    
    if not (has_keyword or has_provider):
        return False
    
    # Filter out common false positives
    false_positives = [
        'machine learning model', 'data analyst position', 'data scientist role',
        'microsoft sql server management', 'microsoft office', 'google docs',
        'google sheets', 'google cloud platform project'
    ]
    
    cert_lower = cert.lower()
    if any(fp in cert_lower for fp in false_positives):
        return False
    
    return True


# Test
if __name__ == "__main__":
    sample = """
    Certifications
    AWS Certified Solutions Architect - Associate (2024)
    Microsoft Certified: Azure Data Scientist Associate
    Google Cloud Professional Data Engineer
    Coursera: Machine Learning Specialization by Andrew Ng
    
    Experience
    Used Microsoft SQL Server Management Studio for database work.
    """
    
    certs = extract_certifications(sample)
    print("Extracted Certifications:")
    for cert in certs:
        print(f"  - {cert}")