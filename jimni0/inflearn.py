import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


service = Service(executable_path="/opt/homebrew/bin/chromedriver")
options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

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

    # Title
    title_el = soup.select_one(
        "#main > section > div.cd-sticky-wrapper > "
        "div.cd-header.cd-header--offline-course.cd-header__not-owned-course > "
        "div.ac-container > div > div.cd-header__right.ac-cd-7.ac-ct-12 > "
        "div.cd-header__title-container.cd-header__title-container--offline > h1"
    )
    title = title_el.get_text(strip=True) if title_el else "N/A"

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

    # Description
    desc_el = soup.select_one("#description")
    description = desc_el.get_text(strip=True) if desc_el else "N/A"

    results.append([title, host, date, url, description])
    time.sleep(0.5)

driver.quit()


with open("inflearn.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "host", "date", "url", "description"])
    writer.writerows(results)

