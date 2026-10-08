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
    """Extract + Summarize links (COMPLETE FEATURE!)"""
    
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
        
        except Exception as e:
            return None
    
    def summarize_with_groq(self, content, url):
        """Send to Groq for AI summary"""
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{
                    "role": "user",
                    "content": f"Summarize this article in 2-3 sentences:\n\n{content}"
                }]
            )
            
            summary = response.choices[0].message.content
            return summary
        
        except Exception as e:
            return f"❌ Groq error: {str(e)}"
    
    def analyze_link(self, url):
        """Complete pipeline: Extract + Summarize"""
        print(f"\n🔗 Analyzing: {url}")
        
        # Step 1: Extract
        print("📖 Extracting content...")
        content = self.extract_content(url)
        
        if not content:
            print("❌ Could not extract content")
            return {
                "url": url,
                "status": "failed",
                "reason": "Could not extract content"
            }
        
        print(f"✅ Extracted {len(content)} characters")
        
        # Step 2: Summarize
        print("🤖 Asking Groq for summary...")
        summary = self.summarize_with_groq(content, url)
        
        print(f"✅ Summary ready!")
        
        return {
            "url": url,
            "status": "success",
            "extracted_length": len(content),
            "summary": summary,
            "ready_for_ara": True
        }

# TEST IT
analyzer = LinkAnalyzer()

print("🚀 LINK ANALYZER FOR ARA\n")
print("="*50)

# Test with one link
test_url = "https://www.bbc.com/news"
result = analyzer.analyze_link(test_url)

print("\n" + "="*50)
print("📊 RESULT:")
print("="*50)
print(f"URL: {result['url']}")
print(f"Status: {result['status']}")

if result['status'] == 'success':
    print(f"\n📄 EXTRACTED: {result['extracted_length']} chars")
    print(f"\n🤖 GROQ SUMMARY:\n{result['summary']}")