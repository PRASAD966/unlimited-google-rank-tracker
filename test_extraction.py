import os
import sys

# Change to the working directory so we can import server.py
sys.path.append(r"C:\Users\kadiy\Downloads\rankproxy 3\rankproxy")
from server import find_keyword_rank
from playwright.sync_api import sync_playwright

def test_single_scrape():
    print("Starting Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # We test with a known target that shows up (like amazon.in for 'Electronics online')
        keyword = 'Electronics online'
        target_domain = 'amazon.in'
        
        print(f"Scraping '{keyword}' for target '{target_domain}'...")
        # Start page=0, max_pages=1 -> Just scrapes page 1
        rank, p_num, link = find_keyword_rank(page, keyword, target_domain, max_pages=2)
        
        if rank:
            print(f"SUCCESS: Rank {rank}, Page {p_num}, Link '{link}'")
        else:
            print("Target not found in the scraped pages.")
            
        browser.close()

if __name__ == "__main__":
    test_single_scrape()
