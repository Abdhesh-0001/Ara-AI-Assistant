import requests
from bs4 import BeautifulSoup

# Fetch a simple webpage
url = "https://example.com"
response = requests.get(url)

# Parse it
soup = BeautifulSoup(response.text, 'html.parser')

# Find all paragraphs
paragraphs = soup.find_all('p')

# Print first 3
for para in paragraphs[:3]:
    print(para.text)