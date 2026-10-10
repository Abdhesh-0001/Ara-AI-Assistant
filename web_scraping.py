import requests
from bs4 import BeautifulSoup
import re
import time
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class LinkAnalyzer:
    """Enhanced - Multiple links + Ara integration ready"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    
    def clean_text(self, text):
        """Clean text"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_content(self, url):
        """Extract article content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try strategies
            content = soup.find('article') or soup.find('main') or \
                      soup.find('div', class_=re.compile(r'content|article|body'))
            
            if content:
                paragraphs = content.find_all('p')
                if paragraphs:
                    cleaned = [self.clean_text(p.text) for p in paragraphs if p.text.strip()]
                    return " ".join(cleaned)[:1500]
            
            # Fallback
            all_p = soup.find_all('p')[1:15]
            if all_p:
                cleaned = [self.clean_text(p.text) for p in all_p if p.text.strip()]
                return " ".join(cleaned)[:1500]
            
            return None
        
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except Exception:
            return None
    
    def summarize_with_groq(self, content):
        """Get AI summary"""
        try:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": f"Summarize in 2-3 sentences:\n\n{content}"
                }]
            )
            return response.choices[0].message.content
        
        except Exception:
            return "❌ Summarization failed"
    
    def analyze_link(self, url):
        """Analyze single link"""
        try:
            # Extract
            content = self.extract_content(url)
            
            if not content:
                return {
                    "url": url,
                    "status": "failed",
                    "reason": "Could not extract content"
                }
            
            # Summarize
            summary = self.summarize_with_groq(content)
            
            return {
                "url": url,
                "status": "success",
                "content_length": len(content),
                "summary": summary,
                "ready_for_ara": True
            }
        
        except Exception as e:
            return {
                "url": url,
                "status": "error",
                "error": str(e)
            }
    
    def analyze_multiple_links(self, urls, verbose=True):
        """Analyze MULTIPLE links with rate limiting"""
        results = []
        
        for i, url in enumerate(urls, 1):
            if verbose:
                print(f"\n📍 [{i}/{len(urls)}] Processing: {url}")
            
            result = self.analyze_link(url)
            results.append(result)
            
            if verbose:
                if result["status"] == "success":
                    print(f"✅ Success - {result['content_length']} chars")
                else:
                    print(f"❌ {result['status']}")
            
            # Rate limit
            if i < len(urls):
                time.sleep(1)
        
        return results
    
    def prepare_for_ara(self, results):
        """Format for Ara display"""
        ara_data = []
        
        for result in results:
            if result["status"] == "success":
                ara_data.append({
                    "url": result["url"],
                    "summary": result["summary"],
                    "display": f"📄 **Link Summary:**\n\n{result['summary']}"
                })
        
        return ara_data

# TEST MULTIPLE LINKS
analyzer = LinkAnalyzer()

print("🚀 MULTI-LINK ANALYZER FOR ARA\n")
print("="*50)

# Multiple URLs
urls = [
    "https://www.bbc.com/news",
    "https://www.python.org/",
    "https://news.ycombinator.com/"
]

# Analyze all
results = analyzer.analyze_multiple_links(urls)

# Prepare for Ara
ara_ready = analyzer.prepare_for_ara(results)

print("\n" + "="*50)
print("📊 READY FOR ARA:")
print("="*50)
print(f"\n✅ Processed: {len(results)} links")
print(f"✅ Success: {len(ara_ready)} links")

for data in ara_ready:
    print(f"\n{data['display']}")