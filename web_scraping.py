import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Remove extra whitespace and newlines"""
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

url = "https://example.com"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find main content
    paragraphs = soup.find_all('p')[:3]
    
    if not paragraphs:
        print("❌ No paragraphs found")
    else:
        print("✅ Extracted content:")
        all_text = []
        for p in paragraphs:
            cleaned = clean_text(p.text)
            all_text.append(cleaned)
            print(f"- {cleaned[:10]}...")  # First 100 chars
        
        # Combine all text
        full_text = " ".join(all_text)
        print(f"\n📊 Total characters: {len(full_text)}")
        print(f"📊 Ready for Groq: {full_text[:200]}...")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")