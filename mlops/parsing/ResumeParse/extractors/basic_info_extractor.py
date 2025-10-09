import re


def extract_basic_info(text: str, extra_urls: list[str] = None) -> dict:
    """
    Extracts basic info like name, emails, phone numbers, and URLs from resume text.
    """
    # Email pattern - more strict to avoid false positives
    EMAIL_RE = re.compile(
        r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    )
    
    # Phone pattern - handles various formats
    PHONE_RE = re.compile(
        r'(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b'
    )
    
    # URL pattern
    URL_RE = re.compile(r'https?://[^\s]+')
    
    # Extract emails
    emails = list(set(EMAIL_RE.findall(text)))
    # Filter out generic/placeholder emails
    emails = [e for e in emails if not any(x in e.lower() for x in ['example.com', 'x@x.com', 'test@'])]
    
    # Extract phone numbers
    phones_raw = PHONE_RE.findall(text)
    phones = []
    for phone in phones_raw:
        # Clean phone number
        clean = re.sub(r'[^\d+]', '', phone)
        # Filter valid phone numbers (7-15 digits)
        if 7 <= len(clean.replace('+', '')) <= 15:
            phones.append(phone.strip())
    phones = list(set(phones))
    
    # Extract URLs from text
    urls = list(set(URL_RE.findall(text)))
    
    # Merge with extra URLs from hyperlinks
    if extra_urls:
        urls.extend(extra_urls)
    urls = list(set(urls))
    
    # Categorize URLs
    linkedin = ""
    github = ""
    
    for url in urls:
        if 'linkedin.com' in url.lower():
            linkedin = url
        elif 'github.com' in url.lower():
            github = url
    
    # Extract name (usually at the top of resume)
    name = extract_name(text)
    
    return {
        "name": name,
        "emails": emails,
        "phones": phones,
        "urls": urls,
        "linkedin": linkedin,
        "github": github
    }


def extract_name(text: str) -> str:
    """
    Extract candidate name - usually the first line or first prominent text.
    Uses heuristics:
    - First non-empty line
    - 2-5 words
    - Capitalized words
    - Not containing common keywords
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return ""
    
    # Check first few lines
    for line in lines[:5]:
        # Skip if line has email, phone, or URL
        if '@' in line or 'http' in line or re.search(r'\d{3,}', line):
            continue
        
        # Skip common headers
        if any(keyword in line.lower() for keyword in [
            'resume', 'cv', 'curriculum', 'profile', 'objective', 
            'education', 'experience', 'skills'
        ]):
            continue
        
        words = line.split()
        
        # Name should be 2-5 words, all capitalized or title case
        if 2 <= len(words) <= 5:
            # Check if mostly capitalized
            cap_words = sum(1 for w in words if w[0].isupper())
            if cap_words >= len(words) * 0.7:
                return line
    
    # Fallback: return first line
    return lines[0] if lines else ""


# Example usage
if __name__ == "__main__":
    sample_text = """
    Musa Bin Arfah
    0309-2753032 | musaarfah2@gmail.com | LinkedIn | GitHub
    
    Education
    Punjab University College of Information and Technology (PUCIT)
    """
    
    result = extract_basic_info(sample_text)
    print(result)