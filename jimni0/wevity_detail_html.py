from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import re
import os

# 저장할 폴더 경로
output_dir = "wevity_html"
os.makedirs(output_dir, exist_ok=True)

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
        page += 1

# HTML 저장
for link in links:
    driver.get(link)
    time.sleep(2)
    try:
        detail_elem = driver.find_element(By.CSS_SELECTOR, '#viewContents')
        html_content = detail_elem.get_attribute('outerHTML')

        match = re.search(r"ix=(\d+)", link)
        file_name = f"wevity_{match.group(1)}.html" if match else "wevity_unknown.html"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    except Exception as e:
        print(f"오류 발생: {e}")
        continue

driver.quit()
