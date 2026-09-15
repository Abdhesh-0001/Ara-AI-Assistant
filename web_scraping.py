import requests
from bs4 import BeautifulSoup

# Example HTML (simplified)
html = """
<html>
  <div class="product">iPhone 15</div>
  <div class="product">Galaxy S24</div>
  <div class="product">Pixel 8</div>
  <div class="product">Pixel 25</div>
  <div id="featured">OnePlus 12</div>
  <div id="featured">OnePlus 13</div>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Find by CLASS (multiple results)
products = soup.find_all(class_='product')
print("Products found:")
for product in products[:3]:
    print(f"  - {product.text}")

# Find by ID (single result)
featureds = soup.find_all(id='featured')
print("featureds found:")
for featured in featureds:
    print(f"  - {featured.text}")