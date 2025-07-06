import re
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time
import pandas as pd
import os
import html

def extract_organizer(soup):
    """주최자 정보를 추출하는 함수"""
    for tag in soup.select("h3, strong, b"):
        if "주최" in tag.get_text():
            for sibling in tag.find_all_next():
                if sibling.name in ["h3", "strong", "b"] and sibling != tag:
                    break
                if sibling.name == "p":
                    text = sibling.get_text(strip=True)
                    if text:
                        return text
                if sibling.name == "ul":
                    items = [li.get_text(strip=True) for li in sibling.find_all("li") if li.get_text(strip=True)]
                    if items:
                        return " / ".join(items)
    return "주최 정보 없음"


def clean_organizer(raw_text):
    """주최자 정보를 정리하는 함수"""
    raw_text = raw_text.strip().replace("：", ":")
    matches = re.findall(r"(주최[^:：]*[:：]\s*[^/]+)", raw_text)
    if not matches:
        return raw_text.strip() if raw_text else "주최 정보 없음"

    orgs = []
    for match in matches:
        _, org_text = match.split(":", 1)
        orgs.extend([o.strip() for o in org_text.split(",") if o.strip()])
    return ", ".join(orgs) if orgs else "주최 정보 없음"


def extract_date_range_string(soup: BeautifulSoup) -> str:
    li_tags = soup.find_all("li", class_="text-body-2")
    for li in li_tags:
        text = li.get_text(strip=True)
        # 날짜 패턴이 포함된 텍스트를 찾아서 원본 그대로 반환
        match = re.search(r"\d{4}\.\d{2}\.\d{2}.*?(?:\d{4}\.\d{2}\.\d{2}|\d{2}:\d{2})", text)
        if match:
            return match.group().strip()
    return "날짜 정보 없음"


def crawl_dacon(limit=None):
    """
    데이콘 대회 정보를 크롤링하는 함수
    
    Args:
        limit (int, optional): 크롤링할 대회 수 제한. None이면 모든 대회
    
    Returns:
        pandas.DataFrame: 크롤링된 대회 정보
    """
    # 첫 번째 단계: 모든 대회 URL 수집
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://dacon.io/competitions")
    time.sleep(2)

    # 수집 시작 후 더보기 클릭
    while True:
        try:
            load_more = driver.find_element(By.CSS_SELECTOR, "#main > button")
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
            time.sleep(0.5)
            load_more.click()
            time.sleep(1.2)

            # 스크롤 다운 강제 → 더 많은 카드 렌더링 유도
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(0.3)

        except:
            break

    # comp div 순회
    comp_divs = driver.find_elements(By.CSS_SELECTOR, "div.comp")
    urls = []
    for div in comp_divs:
        try:
            a_tag = div.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute("href")
            if href:
                urls.append(urljoin("https://dacon.io", href))
        except:
            continue

    driver.quit()

    # 제한이 있다면 적용
    if limit:
        urls = urls[:limit]

    # 두 번째 단계: 각 대회 상세 정보 수집
    results = []
    
    # 새로운 드라이버 생성
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for url in urls:
        try:
            driver.get(url)
            time.sleep(3)  # JS 로딩 시간 기다리기

            soup = BeautifulSoup(driver.page_source, "html.parser")

            title_elem = soup.select_one("h1")
            title = title_elem.text.strip() if title_elem else "제목 없음"

            status_elem = soup.select_one("li.d-inline.text-body-2 span.ms-5")
            status = status_elem.text.strip() if status_elem else ""

            if "마감" in status:
                print(f"⛔ 마감된 대회 스킵: {title}")
                continue

            organizer_raw = extract_organizer(soup)
            organizer_cleaned = clean_organizer(organizer_raw)
            date = extract_date_range_string(soup)

            div = soup.select_one("div.CompetitionDetailTitleSection")
            img_url = None
            if div:
                style = div.get("style", "")
                print(f"[DEBUG] style: {style}")  # 확인용

                style = html.unescape(style)
                m = re.search(r'background-image\s*:\s*url\((["\']?)(.*?)\1\)', style)
                if m:
                    img_url = m.group(2)

            results.append({
                "title": title,
                "date": date,
                "host": organizer_cleaned,
                "url": url,
                "img_url": img_url
            })

            print(f"✅ 수집 완료: {title}")

        except Exception as e:
            print(f"❌ 에러 발생: {url}\n   ↳ {type(e).__name__}: {e}")

    # 크롬 드라이버 종료
    driver.quit()

    # 결과를 DataFrame으로 변환
    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    """스크립트 단독 실행 시: 크롤링 → CSV 저장."""
    print("🚀 Starting Dacon crawling...")
    
    # 테스트용으로 10개만 수집
    df = crawl_dacon(limit=10)
    
    if df.empty:
        print("\n⚠️  수집된 데이터가 없습니다.")
    else:
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join("output", f"dacon_competitions_{timestamp}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"\n🎉 {len(df):,}건 저장 완료 → {out_path}") 