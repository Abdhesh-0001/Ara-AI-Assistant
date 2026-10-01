import requests
from bs4 import BeautifulSoup
import re
import time  # IMPORTANT for rate limiting!

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. Define the URL first
url = "https://example.com"

# 2. Make the request
response = requests.get(url, headers=headers)

print(response.status_code)

def clean_text(text):
    """Remove extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_article(url):
    """Extract main content from article"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find content
        content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
        
        if not content:
            return None
        
        paragraphs = content.find_all('p')
        if not paragraphs:
            return None
        
        cleaned = [clean_text(p.text) for p in paragraphs]
        full_text = " ".join(cleaned)
        
        # Limit length
        max_chars = 1500
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "..."
        
        return full_text
    
    except Exception as e:
        return None

def scrape_multiple_links(urls):
    """Scrape multiple links with rate limiting"""
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n📍 Processing link {i}/{len(urls)}: {url}")
        
        # Extract content
        content = extract_article(url)
        
        if content:
            print(f"✅ Extracted {len(content)} characters")
            results.append({
                "url": url,
                "content": content,
                "status": "success"
            })
        else:
            print(f"❌ Could not extract content")
            results.append({
                "url": url,
                "content": None,
                "status": "failed"
            })
        
        # RATE LIMITING: Wait 2 seconds between requests
        # Respect the website! Don't hammer it!
        if i < len(urls):
            print("⏳ Waiting 2 seconds before next request...")
            time.sleep(2)
    
    return results

# TEST WITH MULTIPLE LINKS
urls = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://w3schools.com"
]

results = scrape_multiple_links(urls)

print("\n" + "="*50)
print("📊 SUMMARY:")
print("="*50)

successful = sum(1 for r in results if r["status"] == "success")
failed = sum(1 for r in results if r["status"] == "failed")

print(f"✅ Successful: {successful}/{len(urls)}")
print(f"❌ Failed: {failed}/{len(urls)}")

for r in results:
    if r["content"]:
        print(f"\n📄 {r['url']}")
        print(f"   Preview: {r['content'][:100]}...")