import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Remove extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_article(url):
    """Extract main content from any article"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find article content (different sites use different tags)
        # Priority: article > main > div.content
        content = soup.find('article')
        if not content:
            content = soup.find('main')
        if not content:
            content = soup.find('div', class_='content')
        
        if not content:
            return None
        
        # Extract all paragraphs
        paragraphs = content.find_all('p')
        
        if not paragraphs:
            return None
        
        # Clean and combine
        cleaned_paragraphs = [clean_text(p.text) for p in paragraphs]
        
        # Join with spaces
        full_article = " ".join(cleaned_paragraphs)
        
        # Limit to reasonable length (for token cost)
        max_chars = 2000
        if len(full_article) > max_chars:
            full_article = full_article[:max_chars] + "..."
        
        return full_article
    
    except requests.exceptions.Timeout:
        return "❌ Website too slow"
    except requests.exceptions.ConnectionError:
        return "❌ No connection"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# TEST IT
article_url = "https://news.ycombinator.com/"
content = extract_article(article_url)

if content:
    print(f"✅ EXTRACTED CONTENT:\n")
    print(content[:500] + "...\n")  # First 500 chars
    print(f"📊 Total length: {len(content)} characters")
    print(f"📊 Ready for Groq: YES")
else:
    print("❌ Could not extract article")