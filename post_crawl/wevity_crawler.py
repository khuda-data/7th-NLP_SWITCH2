import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def init_driver():
    """크롬 드라이버를 초기화하는 함수"""
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=service, options=options)


def crawl_wevity():
    """
    위비티 이벤트 정보를 크롤링하는 함수
    
    Returns:
        pandas.DataFrame: 크롤링된 이벤트 정보 (title, host, date, url 컬럼 포함)
    """
    driver = init_driver()
    cidx_list = [20, 21]
    links = []

    for cidx in cidx_list:
        page = 1
        while True:
            base_url = f"https://www.wevity.com/?c=find&s=1&gub=1&cidx={cidx}&gp={page}"
            driver.get(base_url)
            time.sleep(2)

            event_elements = driver.find_elements(
                By.CSS_SELECTOR,
                "#container .content-area .content-wrap .content > div:nth-child(4) ul li"
            )
            
            if not event_elements:
                break

            stop_page = False
            for elem in event_elements:
                try:
                    date_text = elem.find_element(By.CSS_SELECTOR, "div.day").text
                    # D+ 만나면 이 페이지 이후는 크롤링 불필요
                    if date_text.startswith("D+"):
                        stop_page = True
                        break
                    if date_text.startswith("D-"):
                        href = elem.find_element(By.TAG_NAME, "a").get_attribute("href")
                        links.append(href)
                except Exception:
                    continue

            if stop_page:
                break
            page += 1  # 다음 페이지로 이동

    results = []
    for link in links:
        driver.get(link)
        time.sleep(2)
        try:
            title = driver.find_element(
                By.CSS_SELECTOR,
                "#container .tit-area h6"
            ).text
            host = driver.find_element(
                By.CSS_SELECTOR,
                "#container .content-area .content-wrap .content .cd-area .info ul li:nth-child(3)"
            ).text[5:].strip()
            date = driver.find_element(
                By.CSS_SELECTOR,
                "#container .content-area .content-wrap .content .cd-area .info ul li.dday-area"
            ).text[4:28].strip()
            url = driver.find_element(
                By.CSS_SELECTOR,
                "#container .content-area .content-wrap .content .cd-area .info ul li:nth-child(8)"
            ).text[4:].strip()

            results.append({"title": title, "host": host, "date": date, "url": url})
        except Exception:
            continue

    driver.quit()
    return pd.DataFrame(results)


if __name__ == "__main__":
    print("🚀 Starting Wevity crawling...")
    
    df = crawl_wevity()
    
    if df.empty:
        print("\n⚠️  수집된 데이터가 없습니다.")
    else:
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join("output", f"wevity_competitions_{timestamp}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\n🎉 {len(df):,}건 저장 완료 → {out_path}")
