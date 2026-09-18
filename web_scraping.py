from bs4 import BeautifulSoup

html = """
<html>
  <div class="container">
    <div class="product">iPhone 15</div>
    <div class="product featured">Galaxy S24</div>
    <div class="product">Pixel 8</div>
    <p id="discount">20% OFF</p>
  </div>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Test these selectors:
print("1. All products:")
products = soup.select('.product')
for p in products:
    print(f"  {p.text}")

print("\n2. Only featured product:")
featured = soup.select('.product.featured')
for f in featured:
    print(f"  {f.text}")

print("\n3. Discount text:")
discount = soup.select('#discount')
for d in discount:
    print(f"  {d.text}")

print("\n4. First product only:")
first = soup.select('.product')[:1]
for f in first:
    print(f"  {f.text}")