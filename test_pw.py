import os
from playwright.sync_api import sync_playwright
import time
from dotenv import load_dotenv

load_dotenv()

PROXY_SERVER = os.environ.get('PROXY_SERVER')
PROXY_PORT = os.environ.get('PROXY_PORT')
PROXY_USERNAME = os.environ.get('PROXY_USERNAME')
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')

def test_playwright_proxy():
    print("Testing Playwright with proxy:", PROXY_SERVER)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        proxy_config = {
            "server": f"http://{PROXY_SERVER}:{PROXY_PORT}",
            "username": PROXY_USERNAME,
            "password": PROXY_PASSWORD
        }
        print("Proxy Config:", proxy_config)
        context = browser.new_context(proxy=proxy_config, ignore_https_errors=True)
        page = context.new_page()
        try:
            page.goto("http://api.ip.cc", timeout=20000)
            print("Content:", page.content()[:300])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    test_playwright_proxy()
