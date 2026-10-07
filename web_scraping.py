import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

class NewsFeedScraper:
    """Professional news scraper for Ara"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        self.results = []
    
    def clean_text(self, text):
        """Clean text thoroughly"""
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\n', ' ')
        return text.strip()
    
    def extract_content(self, url):
        """Extract with all strategies"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple strategies
            strategies = [
                lambda: soup.find('article'),
                lambda: soup.find('main'),
                lambda: soup.find('div', class_=re.compile(r'content|article|body')),
            ]
            
            for strategy in strategies:
                content = strategy()
                if content:
                    paragraphs = content.find_all('p')
                    if paragraphs:
                        cleaned = [self.clean_text(p.text) for p in paragraphs if p.text.strip()]
                        text = " ".join(cleaned)
                        return text[:1500]
            
            # Fallback
            all_p = soup.find_all('p')[1:15]
            if all_p:
                cleaned = [self.clean_text(p.text) for p in all_p if p.text.strip()]
                return " ".join(cleaned)[:1500]
            
            return None
        
        except Exception:
            return None
    
    def scrape_news_feed(self, urls, verbose=True):
        """Scrape multiple news sources"""
        self.results = []
        
        for i, url in enumerate(urls, 1):
            if verbose:
                print(f"\n📍 [{i}/{len(urls)}] {url}")
            
            content = self.extract_content(url)
            
            result = {
                "url": url,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "status": "success" if content else "failed",
                "length": len(content) if content else 0
            }
            
            self.results.append(result)
            
            if verbose and content:
                print(f"✅ {len(content)} chars extracted")
            elif verbose:
                print(f"❌ Failed to extract")
            
            # Rate limit
            if i < len(urls):
                time.sleep(1)
        
        return self.results
    
    def get_summary_for_groq(self):
        """Prepare data for Groq summarization"""
        summaries = []
        
        for result in self.results:
            if result["status"] == "success":
                summaries.append({
                    "url": result["url"],
                    "content": result["content"],
                    "ready": True
                })
        
        return {
            "total_scraped": len(self.results),
            "successful": len(summaries),
            "data": summaries
        }

# REAL USAGE FOR ARA
if __name__ == "__main__":
    scraper = NewsFeedScraper()
    
    # News URLs
    news_urls = [
        "https://www.bbc.com/news",
        "https://www.python.org/",
        "https://news.ycombinator.com/"
    ]
    
    print("🚀 NEWS FEED SCRAPER FOR ARA\n")
    print("="*50)
    
    # Scrape
    results = scraper.scrape_news_feed(news_urls)
    
    # Prepare for Groq
    groq_ready = scraper.get_summary_for_groq()
    
    print("\n" + "="*50)
    print("📊 READY FOR GROQ SUMMARIZATION:")
    print("="*50)
    print(f"\n✅ Total scraped: {groq_ready['total_scraped']}")
    print(f"✅ Successful: {groq_ready['successful']}")
    print(f"\n📄 Data ready for Groq: {len(groq_ready['data'])} articles")