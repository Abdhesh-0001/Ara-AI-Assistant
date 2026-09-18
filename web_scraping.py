import requests
from bs4 import BeautifulSoup

html = """
<html>
  <div class="product">
    <span class="name">iPhone 15</span>
    <span class="price">$999</span>
  </div>
  <div class="product">
    <span class="name">Galaxy S24</span>
    <!-- No price tag for this one! -->
  </div>
  <div class="product">
    <span class="name">Pixel 8</span>
    <span class="price">$799</span>
  </div>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Find all products
products = soup.find_all(class_='product')

for product in products:
    # Get name (safe - always exists)
    name_tag = product.find(class_='name')
    name = name_tag.text if name_tag else "Unknown"
    
    # Get price (might not exist!)
    price_tag = product.find(class_='price')
    price = price_tag.text if price_tag else "Price unavailable"
    
    print(f"Product: {name}")
    print(f"Price: {price}")
    print("---")