from playwright.async_api import async_playwright
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin
import pandas as pd
import re
import time
from datetime import datetime
import asyncio
import os

# ---------------------------------------------------------------------------
# 핵심 파라미터 (필요시 아래 값만 수정해 사용)
# ---------------------------------------------------------------------------
SECTION_HINTS = ("[배경]", "[주제]", "[설명]", "[참가", "[주최", "[시상")
TERMS_PATTERN = re.compile(r"제\s*\d+\s*조")      # 약관 조문 식별용

# ---------------------------------------------------------------------------
# 1) 상세 페이지 HTML 중 ql-editor 블록 추출 & 정제
# ---------------------------------------------------------------------------
async def fetch_clean_body(url: str) -> str:
    """데이콘 상세 페이지에서 *소개 영역*으로 보이는 div.ql-editor 1개를 골라 HTML 반환"""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/122.0.0.0 Safari/537.36")
            )
            page = await context.new_page()
            await page.goto(url, wait_until="load", timeout=40000)
            await page.wait_for_selector("div.ql-editor", timeout=15000)

            # --- ① 모든 ql-editor 후보 수집 ---
            nodes = await page.query_selector_all("div.ql-editor")
            html_candidates: list[str] = []
            for n in nodes:
                try:
                    html_candidates.append(await n.inner_html())
                except Exception:
                    continue
            await browser.close()

            if not html_candidates:
                return ""  # nothing found

            # --- ② 헤더 키워드 포함 블록 우선 선택 ---
            def contains_section(html: str) -> bool:
                text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
                return any(h in text for h in SECTION_HINTS)

            primary = next((h for h in html_candidates if contains_section(h)), None)

            # --- ③ fallback: 약관(제 n 조)·길이 2000자↑ 제외 후 가장 짧은 블록 ---
            if primary is None:
                def looks_like_terms(html: str) -> bool:
                    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
                    return TERMS_PATTERN.search(text[:120]) is not None or len(text) > 2000
                filtered = [h for h in html_candidates if not looks_like_terms(h)]
                primary = min(filtered, key=len) if filtered else min(html_candidates, key=len)

            # --- ④ 불필요 태그 정리 ---
            soup = BeautifulSoup(f"<div class='ql-editor'>{primary}</div>", "html.parser")
            for tag in soup.find_all(['script', 'svg', 'path', 'iframe', 'noscript', 'br']):
                tag.decompose()
            return str(soup.div.prettify())

    except Exception as e:
        print(f"[HTML 파싱 실패] {url} - {e}")
        return ""

# ---------------------------------------------------------------------------
# 2) 주최자·날짜 등 메타데이터 추출 함수들
# ---------------------------------------------------------------------------

def extract_organizer(soup: BeautifulSoup) -> str:
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


def clean_organizer(raw_text: str) -> str:
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
        match = re.search(r"\d{4}\.\d{2}\.\d{2}\s*[~\-]\s*\d{4}\.\d{2}\.\d{2}(?:\s*\d{2}:\d{2})?", text)
        if match:
            raw = match.group()
            date_parts = re.findall(r'\d{4}\.\d{2}\.\d{2}', raw)
            if len(date_parts) == 2:
                start = datetime.strptime(date_parts[0], "%Y.%m.%d").strftime("%Y-%m-%d")
                end = datetime.strptime(date_parts[1], "%Y.%m.%d").strftime("%Y-%m-%d")
                return f"{start} ~ {end}"
            return raw
    return "날짜 정보 없음"

# ---------------------------------------------------------------------------
# 3) 메인 크롤링 루틴
# ---------------------------------------------------------------------------
async def crawl_dacon(limit: int | None = None) -> pd.DataFrame:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://dacon.io/competitions")
    time.sleep(2)

    # 모든 대회 로드 ("더보기" 버튼 반복 클릭)
    while True:
        try:
            load_more = driver.find_element(By.CSS_SELECTOR, "#main > button")
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
            time.sleep(0.4)
            load_more.click(); time.sleep(1.0)
            driver.execute_script("window.scrollBy(0, 1500);")
        except Exception:
            break

    urls = []
    for div in driver.find_elements(By.CSS_SELECTOR, "div.comp"):
        try:
            href = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            if href:
                urls.append(urljoin("https://dacon.io", href))
        except Exception:
            continue
    driver.quit()

    # 상세 페이지 크롤
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    results = []
    for url in (urls if limit is None else urls[:limit]):
        try:
            driver.get(url); time.sleep(2.5)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            title = soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else "제목 없음"
            status = soup.select_one("li.d-inline.text-body-2 span.ms-5")
            if status and "마감" in status.get_text(strip=True):
                print(f"⛔ 마감 스킵: {title}"); continue

            organizer = clean_organizer(extract_organizer(soup))
            date_range = extract_date_range_string(soup)
            html_content = await fetch_clean_body(url)

            results.append({
                "title": title,
                "date":  date_range,
                "host":  organizer,
                "url":   url,
                "html":  html_content,
            })
            print(f"✅ 완료: {title}")
        except Exception as e:
            print(f"❌ 오류: {url} → {e}")
            continue
    driver.quit()
    return pd.DataFrame(results)

# ---------------------------------------------------------------------------
# 4) main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    LIMIT = 10       # ▶︎ 숫자 입력하면 최신 n건만 수집
    df = asyncio.run(crawl_dacon(limit=LIMIT))

    if df.empty:
        print("⚠️  수집 결과가 없습니다.")
    else:
        os.makedirs("output", exist_ok=True)
        fname = f"dacon_competitions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        fpath = os.path.join("output", fname)
        df.to_csv(fpath, index=False, encoding="utf-8-sig")
        print(f"🎉 저장 완료 → {fpath} ({len(df):,} rows)")