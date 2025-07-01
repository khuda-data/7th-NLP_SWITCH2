from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

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

        results.append([title, date, host, url])
    except Exception as e:
        continue  # 일부 카드에 누락된 요소가 있을 수 있으므로 무시

driver.quit()

# 3. CSV 저장
with open("dev_event_data.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "date", "host", "url"])
    writer.writerows(results)

print("✅ 저장 완료: dev_event_data.csv")