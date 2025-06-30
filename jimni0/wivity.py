from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

service = Service(executable_path="/opt/homebrew/bin/chromedriver")
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=options)

# 크롤링할 페이지
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

        results.append([title, host, date, url])
    except Exception:
        continue

with open("wevity_events.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "host", "date", "url"])
    writer.writerows(results)

print(results)
driver.quit()
