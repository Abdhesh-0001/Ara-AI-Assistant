import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://news.ycombina.com/"

try:
    response = requests.get(url, timeout=5)
      # Raise error if not 200
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find articles
    articles = soup.select('.titleline')[:5]
    
    for article in articles:
        # Safely extract title
        title_tag = article.select_one('a')
        title = title_tag.text if title_tag else "No title"
        
        # Safely extract URL
        url_href = title_tag.get('href') if title_tag else "No URL"
        
        print(f"Title: {title}")
        print(f"URL: {url_href}")
        print("---")
        
except requests.exceptions.Timeout:
    print("❌ Website took too long to respond")
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to website")
except Exception as e:
    print(f"❌ Error: {str(e)}")