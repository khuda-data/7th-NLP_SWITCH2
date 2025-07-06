import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time


def crawl_devEvent():
    """
    개발자 이벤트 정보를 크롤링하는 함수
    
    Returns:
        pandas.DataFrame: 크롤링된 이벤트 정보 (title, date, host, url 컬럼 포함)
    """
    # 1. 브라우저 설정
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://dev-event.vercel.app/events")

    time.sleep(5)  # 초기 로딩 대기

    # 2. 이벤트 블록 가져오기
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
        except Exception as e:
            continue  # 일부 카드에 누락된 요소가 있을 수 있으므로 무시

    driver.quit()

    return pd.DataFrame(results)


if __name__ == "__main__":
    print("🚀 Starting DevEvent crawling...")
    
    df = crawl_devEvent()
    
    if df.empty:
        print("\n⚠️  수집된 데이터가 없습니다.")
    else:
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join("output", f"devEvent_competitions_{timestamp}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\n🎉 {len(df):,}건 저장 완료 → {out_path}")