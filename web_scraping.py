import requests
from bs4 import BeautifulSoup
import re
import time

def clean_text(text):
    """Remove extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_article_smart(url):
    """Try multiple strategies to extract content"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # STRATEGY 1: Look for article tags
        content = soup.find('article')
        if content:
            paragraphs = content.find_all('p')
            if paragraphs:
                cleaned = [clean_text(p.text) for p in paragraphs]
                return " ".join(cleaned)[:1500]
        
        # STRATEGY 2: Look for main tag
        content = soup.find('main')
        if content:
            paragraphs = content.find_all('p')
            if paragraphs:
                cleaned = [clean_text(p.text) for p in paragraphs]
                return " ".join(cleaned)[:1500]
        
        # STRATEGY 3: Look for divs with content class
        content = soup.find('div', class_=re.compile(r'content|article|body'))
        if content:
            paragraphs = content.find_all('p')
            if paragraphs:
                cleaned = [clean_text(p.text) for p in paragraphs]
                return " ".join(cleaned)[:1500]
        
        # STRATEGY 4: Just get ALL paragraphs (fallback)
        all_paragraphs = soup.find_all('p')[1:15]  # Skip first (usually nav), limit to 15
        if all_paragraphs:
            cleaned = [clean_text(p.text) for p in all_paragraphs]
            text = " ".join(cleaned)
            return text[:1500] if text else None
        
        return None
    
    except requests.exceptions.Timeout:
        return "❌ Timeout"
    except requests.exceptions.ConnectionError:
        return "❌ No connection"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def analyze_website(url):
    """Analyze which strategy worked"""
    content = extract_article_smart(url)
    
    if content and not content.startswith("❌"):
        return {
            "url": url,
            "success": True,
            "length": len(content),
            "preview": content[:150] + "..."
        }
    else:
        return {
            "url": url,
            "success": False,
            "error": content
        }

# TEST WITH DIFFERENT WEBSITES
test_urls = [
    "https://www.bbc.com/news",
    "https://www.theguardian.com/us",
    "https://news.ycombinator.com/"
]

print("🔍 TESTING DIFFERENT WEBSITES:\n")

for url in test_urls:
    result = analyze_website(url)
    
    print(f"URL: {url}")
    if result["success"]:
        print(f"✅ SUCCESS - Length: {result['length']} chars")
        print(f"Preview: {result['preview']}\n")
    else:
        print(f"❌ FAILED - {result['error']}\n")
    
    time.sleep(1)  # Rate limit