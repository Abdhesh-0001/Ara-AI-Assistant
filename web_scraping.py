# FINAL TEST: Complete scraper + ready for Ara integration
import requests
from bs4 import BeautifulSoup
import re
import time

class ArticleScraper:
    """Complete scraper combining all techniques"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    
    def clean_text(self, text):
        """Remove extra whitespace"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_content(self, url):
        """Extract article with multiple strategies"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Strategy 1: article tag
            content = soup.find('article')
            if content and content.find_all('p'):
                return self._get_paragraphs(content)
            
            # Strategy 2: main tag
            content = soup.find('main')
            if content and content.find_all('p'):
                return self._get_paragraphs(content)
            
            # Strategy 3: div with content class
            content = soup.find('div', class_=re.compile(r'content|article|body'))
            if content and content.find_all('p'):
                return self._get_paragraphs(content)
            
            # Strategy 4: all paragraphs fallback
            all_p = soup.find_all('p')[1:15]
            if all_p:
                return self._get_paragraphs_list(all_p)
            
            return None
        
        except requests.exceptions.Timeout:
            return None
        except Exception:
            return None
    
    def _get_paragraphs(self, element):
        """Extract and clean paragraphs"""
        paragraphs = element.find_all('p')
        cleaned = [self.clean_text(p.text) for p in paragraphs if p.text.strip()]
        text = " ".join(cleaned)
        return text[:1500] if text else None
    
    def _get_paragraphs_list(self, paragraphs):
        """Extract from list of paragraphs"""
        cleaned = [self.clean_text(p.text) for p in paragraphs if p.text.strip()]
        text = " ".join(cleaned)
        return text[:1500] if text else None
    
    def scrape_multiple(self, urls):
        """Scrape multiple URLs with rate limiting"""
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n📍 [{i}/{len(urls)}] Scraping: {url}")
            
            content = self.extract_content(url)
            
            if content:
                print(f"✅ Success - {len(content)} chars")
                results.append({
                    "url": url,
                    "content": content,
                    "status": "success"
                })
            else:
                print(f"❌ Failed")
                results.append({
                    "url": url,
                    "content": None,
                    "status": "failed"
                })
            
            # Rate limit
            if i < len(urls):
                time.sleep(1)
        
        return results

# TEST IT
scraper = ArticleScraper()

urls = [
    "https://www.bbc.com/news",
    "https://news.ycombinator.com/",
    "https://www.python.org/"
]

print("🚀 ARTICLE SCRAPER TOOL\n")
print("="*50)

results = scraper.scrape_multiple(urls)

print("\n" + "="*50)
print("📊 RESULTS:")
print("="*50)

success = sum(1 for r in results if r["status"] == "success")
print(f"\n✅ Successful: {success}/{len(urls)}")

for r in results:
    if r["content"]:
        print(f"\n📄 {r['url']}")
        print(f"   Length: {len(r['content'])} chars")
        print(f"   Preview: {r['content'][:100]}...")

  

def test_scraper_for_ara():
    """Test if scraper works for Ara"""
    
    scraper = ArticleScraper()
    
    # User gives link
    user_link = "https://www.bbc.com/news"
    
    # Step 1: Scrape
    content = scraper.extract_content(user_link)
    
    if not content:
        return "❌ Could not extract content from link"
    
    # Step 2: Prepare for Groq
    prepared = {
        "url": user_link,
        "content": content,
        "length": len(content),
        "ready_for_groq": True
    }
    
    return prepared

# TEST
result = test_scraper_for_ara()
print("📊 SCRAPER READY FOR ARA:")
print(result)