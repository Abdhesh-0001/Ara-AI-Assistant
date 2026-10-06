# FINAL TEST: Complete scraper + ready for Ara integration

from ArticleScraper import ArticleScraper  # Your class from Exercise 11

def test_scraper_for_ara():
    """Test if scraper works for Ara"""
    
    scraper = ArticleScraper()
    
    # User gives link
    user_link = "https://www.bbc.com/news"
    
    # Step 1: Scrape
    content = scraper.extract_content(user_link)
    
    if not content:
        return "❌ Could not extract content from link"
    
    # Step 2: Prepare for Groq
    prepared = {
        "url": user_link,
        "content": content,
        "length": len(content),
        "ready_for_groq": True
    }
    
    return prepared

# TEST
result = test_scraper_for_ara()
print("📊 SCRAPER READY FOR ARA:")
print(result)