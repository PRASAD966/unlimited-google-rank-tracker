from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from datetime import datetime
import os, random, time, platform, subprocess

# ---------------- CONFIG ----------------
EXCEL_FILE = "results.xlsx"
MAX_PAGES = 500
HEADLESS = False  # Keep False to avoid CAPTCHA
DELAY_RANGE = (6, 12)  # human-like delays
# ----------------------------------------

# ---------- CREATE DRIVER ----------
def create_driver():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")

    ua = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    ])
    chrome_options.add_argument(f"user-agent={ua}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=en-IN")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    stealth(driver, languages=["en-IN", "en"], vendor="Google Inc.",
            platform="Win32", webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    driver.set_window_size(1200, 800)
    return driver

# ---------- FIND RANK ----------
def find_keyword_rank(driver, keyword, domain, location):
    rank, page_found = None, None

    for page in range(MAX_PAGES):
        # Skip after 10 pages
        if page >= 10:
            print(f"⚠️ Skipping '{keyword}' after 10 pages (not found)")
            break

        start = page * 10
        search_url = f"https://www.google.com/search?q={keyword}&hl=en&gl={location}&start={start}"
        driver.get(search_url)
        time.sleep(random.uniform(*DELAY_RANGE))

        # Handle consent popup
        try:
            consent = driver.find_elements(By.XPATH, "//button//div[contains(text(), 'Accept all')]")
            if consent:
                consent[0].click()
                time.sleep(2)
        except:
            pass

        # Detect CAPTCHA
        if "captcha" in driver.page_source.lower() or "sorry/index" in driver.current_url.lower():
            input("⚠️ CAPTCHA detected! Solve manually in browser, then press ENTER to continue...")

        # Get search results
        results = driver.find_elements(By.CSS_SELECTOR, "a[jsname='UWckNb'], div.yuRUbf > a")
        for idx, r in enumerate(results, start=1 + page*10):
            href = r.get_attribute("href")
            if href and domain in href:
                rank, page_found = idx, page + 1
                return rank, page_found

    return rank, page_found

# ---------- SAVE RESULTS ----------
def save_to_excel(domain, results):
    green = PatternFill(start_color="00C6EFCE", end_color="00C6EFCE", fill_type="solid")
    yellow = PatternFill(start_color="00FFEB9C", end_color="00FFEB9C", fill_type="solid")
    red = PatternFill(start_color="00FFC7CE", end_color="00FFC7CE", fill_type="solid")

    # Try saving; handle if file is open
    while True:
        try:
            wb = Workbook()
            ws = wb.active
            ws.append(["URL", "Keyword", "Page", "Rank"])

            for keyword, page, rank in results:
                ws.append([domain, keyword, page if page else "N/A", rank if rank else "Not Found"])
                cell = ws.cell(row=ws.max_row, column=4)
                try:
                    r = int(rank)
                    if 1 <= r <= 3: cell.fill = green
                    elif 4 <= r <= 10: cell.fill = yellow
                    else: cell.fill = red
                except:
                    cell.fill = red

            wb.save(EXCEL_FILE)
            print(f"\n✅ Results saved to {EXCEL_FILE}")
            break
        except PermissionError:
            print(f"⚠️ Cannot save {EXCEL_FILE} because it is open. Please close Excel and press ENTER...")
            input()

# ---------- OPEN EXCEL ----------
def open_excel():
    path = os.path.abspath(EXCEL_FILE)
    try:
        if platform.system() == "Windows": os.startfile(path)
        elif platform.system() == "Darwin": subprocess.call(["open", path])
        else: subprocess.call(["xdg-open", path])
    except:
        pass

# ---------- MAIN ----------
def main():
    website = input("Enter your website URL (e.g. https://example.com): ").strip()
    domain = website.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")

    # ✅ Location input added
    location = input("Enter search location (e.g., 'in' for India, 'us' for USA): ").strip().lower() or "in"

    keywords_file = input("Enter path to keywords.txt file: ").strip()
    if not os.path.exists(keywords_file):
        exit("❌ File not found.")

    with open(keywords_file, "r", encoding="utf-8") as f:
        keywords = [k.strip() for k in f if k.strip()]

    print(f"\n📂 Loaded {len(keywords)} keywords for domain '{domain}' ({location.upper()})")
    print("ℹ️ Browser will open — please don’t close it during the search.\n")

    driver = create_driver()
    results = []

    try:
        for i, kw in enumerate(keywords, 1):
            print(f"[{i}/{len(keywords)}] Searching: '{kw}' ...")
            rank, page_num = find_keyword_rank(driver, kw, domain, location)
            if rank:
                print(f" → Found on page {page_num} at position #{rank}")
            else:
                print(f" ❌ Not found within 50 pages. Skipped '{kw}'.")
            results.append((kw, page_num, rank))
    finally:
        driver.quit()

    save_to_excel(domain, results)
    open_excel()
    print("\n🎯 All done!")

# ---------- RUN ----------
if __name__ == "__main__":
    main()
