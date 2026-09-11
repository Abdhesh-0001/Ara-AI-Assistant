import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links
links = soup.find_all('a')

# Extract and print the first 3 links
for link in links[:3]:
    # Each link has:
    # - link.text (the text shown)
    # - link.get('href') (the actual URL)
    
    text = link.text
    url_href = link.get('href')
    
    print(f"Text: {text}")
    print(f"URL: {url_href}")
    print("---")