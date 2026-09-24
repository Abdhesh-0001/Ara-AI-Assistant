import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Remove extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Scrape a real news source
url = "https://news.ycombinator.com/"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get top 3 stories
    stories = soup.select('.titleline')[:3]
    
    if not stories:
        print("❌ No stories found")
    else:
        print("✅ TOP 3 NEWS STORIES:\n")
        
        for i, story in enumerate(stories, 1):
            # Extract title and URL
            link = story.select_one('a')
            
            if link:
                title = clean_text(link.text)
                story_url = link.get('href', 'No URL')
                
                # Make relative URLs absolute
                if story_url.startswith('/'):
                    story_url = "https://news.ycombinator.com" + story_url
                
                print(f"{i}. Title: {title}")
                print(f"   URL: {story_url}")
                print(f"   Status: ✅ Ready for summarization\n")
            else:
                print(f"{i}. ❌ Could not extract story")
    
except requests.exceptions.Timeout:
    print("❌ Website too slow")
except requests.exceptions.ConnectionError:
    print("❌ No internet connection")
except Exception as e:
    print(f"❌ Error: {str(e)}")