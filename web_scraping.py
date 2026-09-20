import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all quotes using CSS selector
quotes = soup.select('.quote')

for quote in quotes[:3]:  # First 3 only
    text = quote.select_one('.text').text
    author = quote.select_one('.author').text
    
    print(f"Quote: {text}")
    print(f"Author: {author}")
    print("---")