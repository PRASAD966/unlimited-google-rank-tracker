from playwright.sync_api import sync_playwright
import time
import urllib.parse

def test_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        keyword = "ipad"
        # India specific Google search
        url = f"https://www.google.co.in/search?q={urllib.parse.quote(keyword)}&hl=en&gl=in"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="domcontentloaded")
        
        time.sleep(5) # Give it some time to load everything
        
        print("\n--- RESULTS FOUND ---")
        # 1. Try to find all A with H3
        links = page.locator("#search a:has(h3)").all()
        print(f"Found {len(links)} links with H3 in #search")
        
        for i, link in enumerate(links):
            try:
                href = link.get_attribute("href")
                inner_text = link.inner_text().replace("\n", " ")
                
                # Check for "Sponsored" in parents
                is_sponsored = page.evaluate("(el) => { \
                    let p = el; \
                    for(let i=0; i<8; i++) { \
                        if(!p) break; \
                        if(p.innerText && (p.innerText.toLowerCase().includes('sponsored') || p.innerText.toLowerCase().includes('ads'))) { \
                            return true; \
                        } \
                        p = p.parentElement; \
                    } \
                    return false; \
                }", link)
                
                type_label = "[ORGANIC]"
                if is_sponsored:
                    type_label = "[SPONSORED]"
                
                print(f"{i+1}. {type_label} {inner_text} -> {href}")
            except Exception as e:
                print(f"Error parsing link {i}: {e}")
                
        browser.close()

if __name__ == "__main__":
    test_search()
