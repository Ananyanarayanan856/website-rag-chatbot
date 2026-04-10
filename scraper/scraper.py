import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_page(driver, url, timeout=20):
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        title = driver.title.strip()

        try:
            meta_desc = driver.find_element(
                By.XPATH, '//meta[@name="description"]'
            ).get_attribute("content") or ""
        except Exception:
            meta_desc = ""

        headings = []
        for tag in ["h1", "h2", "h3"]:
            for el in driver.find_elements(By.TAG_NAME, tag):
                text = el.text.strip()
                if text:
                    headings.append({"tag": tag, "text": text})

        paragraphs = []
        for el in driver.find_elements(By.TAG_NAME, "p"):
            text = el.text.strip()
            if text and len(text) > 20:
                paragraphs.append(text)

        nav_links = []
        try:
            nav = driver.find_element(By.TAG_NAME, "nav")
            for a in nav.find_elements(By.TAG_NAME, "a"):
                href = a.get_attribute("href") or ""
                text = a.text.strip()
                if href and text:
                    nav_links.append({"text": text, "href": href})
        except Exception:
            pass

        all_links = []
        for el in driver.find_elements(By.TAG_NAME, "a"):
            href = el.get_attribute("href") or ""
            text = el.text.strip()
            if href.startswith("http"):
                all_links.append({"text": text, "href": href})

        images = []
        for el in driver.find_elements(By.TAG_NAME, "img"):
            src = el.get_attribute("src") or ""
            alt = el.get_attribute("alt") or ""
            if src:
                images.append({"src": src, "alt": alt})

        try:
            body_text = driver.find_element(By.TAG_NAME, "body").text.strip()
        except Exception:
            body_text = ""

        return {
            "url": url,
            "status": "success",
            "title": title,
            "meta_description": meta_desc,
            "headings": headings,
            "paragraphs": paragraphs,
            "nav_links": nav_links,
            "all_links": all_links,
            "images": images,
            "body_text": body_text,
        }

    except TimeoutException:
        return {"url": url, "status": "timeout", "error": "Page load timed out"}
    except WebDriverException as e:
        return {"url": url, "status": "error", "error": str(e)}
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}


def main():
    INPUT_FILE  = "sitemap_urls.json"
    OUTPUT_FILE = "scraped_data.json"
    DELAY       = 2

    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    if not isinstance(urls, list):
        print("[ERROR] Expected a JSON array of URLs.")
        return

    print(f"[INFO] Loaded {len(urls)} URLs from {INPUT_FILE}\n")

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
        done = {r["url"] for r in results}
        urls = [u for u in urls if u not in done]
        print(f"[INFO] Resuming — {len(done)} done, {len(urls)} remaining\n")
    else:
        results = []

    if not urls:
        print("[INFO] All URLs already scraped!")
        return

    driver = get_driver()

    try:
        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] {url}")
            data = scrape_page(driver, url)
            results.append(data)

            if data["status"] == "success":
                print(f"  ✓  {data['title'][:70]}")
                print(f"     {len(data['paragraphs'])} paragraphs | "
                      f"{len(data['headings'])} headings | "
                      f"{len(data['all_links'])} links")
            else:
                print(f"  ✗  {data['status']}: {data.get('error','')[:80]}")

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            time.sleep(DELAY)

    finally:
        driver.quit()

    print(f"\n✅  Done! {len(results)} pages saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()