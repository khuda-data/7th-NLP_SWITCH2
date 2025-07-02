# devEvent_crawler.py

import os
import asyncio
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time


async def fetch_clean_body(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await page.goto(url, wait_until="load", timeout=40000)
            await page.wait_for_selector("body", timeout=15000)
            raw_body_html = await page.inner_html("body")
            await browser.close()

        soup = BeautifulSoup(f"<body>{raw_body_html}</body>", "html.parser")
        for tag in soup.find_all(['script', 'svg', 'path', 'iframe', 'noscript', 'br', 'nav']):
            tag.decompose()
        if soup.body is not None:
            return str(soup.body.prettify())
        else:
            return ""
    except Exception as e:
        print(f"[❌ HTML 파싱 실패] {url} - {e}")
        return ""


async def crawl_devEvent():
    # 1. Selenium으로 dev-event 사이트 크롤링
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://dev-event.vercel.app/events")
    time.sleep(5)  # 초기 로딩 대기

    cards = driver.find_elements(By.CSS_SELECTOR, "a")
    results = []

    for card in cards:
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, "div.Item_item__content__title__94_8Q")
            date_elem = card.find_element(By.CSS_SELECTOR, "span.Item_date__date__CoMqV")
            host_elem = card.find_element(By.CSS_SELECTOR, "span.Item_host__3dy8_")
            url = card.get_attribute("href")

            title = title_elem.text.strip()
            date = date_elem.text.strip()
            host = host_elem.text.strip()
            results.append({"title": title, "date": date, "host": host, "url": url})
        except:
            continue

    driver.quit()

    # 2. HTML 파싱 추가
    for row in results:
        row["html"] = await fetch_clean_body(row["url"])

    return pd.DataFrame(results)


if __name__ == "__main__":
    """스크립트 단독 실행 시: 크롤링 → CSV 저장."""
    print("🚀 개발자 이벤트 크롤링 시작...")
    
    async def main():
        df = await crawl_devEvent()
        
        if df.empty:
            print("\n⚠️  수집된 데이터가 없습니다.")
        else:
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join("output", f"devEvent_events_{timestamp}.csv")
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
            print(f"\n🎉 {len(df):,}건 저장 완료 → {out_path}")
    
    asyncio.run(main())