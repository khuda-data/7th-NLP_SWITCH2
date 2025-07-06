import os
from datetime import datetime
from bs4 import BeautifulSoup
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
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=service, options=options)


def crawl_inflearn():
    """
    인프런 오프라인 강좌 정보를 크롤링하는 함수
    
    Returns:
        pandas.DataFrame: 크롤링된 강좌 정보 (title, host, date, url 컬럼 포함)
    """
    driver = init_driver()
    
    # 오프라인 강좌 리스트 페이지 무한 스크롤
    driver.get("https://www.inflearn.com/courses?types=OFFLINE")
    time.sleep(2)
    prev_count = -1
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/course/')]")
        if len(cards) == prev_count:
            break
        prev_count = len(cards)

    links = list({c.get_attribute("href") for c in cards if c.get_attribute("href")})

    results = []
    for url in links:
        if not url:  # url이 None인 경우 건너뛰기
            continue
        driver.get(url)
        time.sleep(1)  
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 모집마감 체크
        badge_el = soup.select_one(
            "#main > section > div.cd-sticky-wrapper > "
            "div.cd-header.cd-header--offline-course.cd-header__not-owned-course > "
            "div.ac-container > div > div.cd-header__left.ac-cd-5.ac-ct-12 > "
            "div > div.cd-header__offline-badges > "
            "span.cd-header__thumbnail-badge.cd-header__not-recruiting-badge"
        )
        if badge_el: 
            continue

        # Title, 제목 뒤의 대시보드 글자 제거 위한 변경
        title_el = soup.select_one(
            "#main > section > div.cd-sticky-wrapper > "
            "div.cd-header.cd-header--offline-course.cd-header__not-owned-course > "
            "div.ac-container > div > div.cd-header__right.ac-cd-7.ac-ct-12 > "
            "div.cd-header__title-container.cd-header__title-container--offline > h1"
        )
        # title = title_el.get_text(strip=True) if title_el else "N/A"
        title = next(title_el.stripped_strings, "N/A") if title_el else "N/A"

        # Host
        host_el = soup.select_one(
            "#main > section > div.cd-sticky-wrapper > "
            "div.cd-header.cd-header--offline-course.cd-header__not-owned-course > "
            "div.ac-container > div > div.cd-header__right.ac-cd-7.ac-ct-12 > "
            "div.cd-header__instructors.cd-header__sub-row.cd-header__instructors--offline > a"
        )
        host = host_el.get_text(strip=True) if host_el else "N/A"

        # Date
        date_el = soup.select_one(
            "#main > section > div.cd-sticky-wrapper > "
            "div.cd-mb-information.e-cd-mb-information > "
            "div.cd-floating__info--wrapper > dl:nth-child(1) > div:nth-child(1) > dd"
        )
        date = date_el.get_text(strip=True) if date_el else "N/A"

        # img_url
        img_el = soup.select_one("img.ac-gif__img")
        img_url = img_el["src"] if img_el else "N/A"

        results.append({
            "title": title,
            "host": host,
            "date": date,
            "url": url,
            "img_url": img_url
        })
        time.sleep(0.5)

    driver.quit()
    return pd.DataFrame(results)


if __name__ == "__main__":
    print("🚀 Starting Inflearn crawling...")
    
    df = crawl_inflearn()
    
    if df.empty:
        print("\n⚠️  수집된 데이터가 없습니다.")
    else:
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join("output", f"inflearn_courses_{timestamp}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\n🎉 {len(df):,}건 저장 완료 → {out_path}")

