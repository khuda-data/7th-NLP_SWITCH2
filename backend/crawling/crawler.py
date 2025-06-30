from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_clean_body(url: str, output_file: str = "body_cleaned.html"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        raw_body_html = page.inner_html("body")
        browser.close()

    soup = BeautifulSoup(f"<body>{raw_body_html}</body>", "html.parser")

    for tag in soup.find_all(['script', 'svg', 'path', 'iframe', 'noscript', 'br', 'nav']):
        tag.decompose()

    cleaned_body = soup.body.prettify()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_body)

    print(f"✅ 필터링된 <body>를 '{output_file}'에 저장했습니다.")

if __name__ == "__main__":
    target_url = input("크롤링할 URL을 입력하세요: ").strip()
    fetch_clean_body(target_url)