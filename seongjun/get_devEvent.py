from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

def fetch_clean_body(url: str, output_file: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            print(f"▶️ 접속 시도: {url}")

            # 페이지 로드 및 명시적 대기
            page.goto(url, wait_until="load", timeout=40000)
            try:
                page.wait_for_selector("body", timeout=15000)
            except:
                print(f"⚠️ body 태그 대기 실패 - {url}")

            # body 내용 추출
            raw_body_html = page.inner_html("body")
            browser.close()

        # 불필요한 태그 제거
        soup = BeautifulSoup(f"<body>{raw_body_html}</body>", "html.parser")
        for tag in soup.find_all(['script', 'svg', 'path', 'iframe', 'noscript', 'br', 'nav']):
            tag.decompose()

        cleaned_body = soup.body.prettify()

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_body)

        print(f"✅ 저장 완료: {output_file}")
    except Exception as e:
        print(f"❌ 에러 발생 ({url}): {e}")

if __name__ == "__main__":
    url_list = [
        "https://event-us.kr/tsbackendmeetup/event/104517",
        "https://www.instagram.com/official.bdaa/p/DK1j16shlnR",
        "https://www.meetup.com/awskrug/events/308274179/",
        "https://www.allforyoung.com/posts/65275",
        "https://eduhancom.com/",
        "https://ausg.me/apply",
        "https://www.meetup.com/awskrug/events/308226383/",
        "https://onoffmix.com/event/325883",
        "https://event-us.kr/susc/event/105371",
        "https://www.wanted.co.kr/events/pre_challenge_be_32",
        "https://onoffmix.com/event/325649",
        "https://event-us.kr/susc/event/106768",
        "https://www.qa-korea.com/qaconference2025",
        "https://developer.apple.com/events/view/TCSPG9PN8Y/dashboard",
        "https://www.meetup.com/awskrug/events/308647412",
        "https://rsvp.withgoogle.com/events/2025-h2-google-cloud-ai-study-jam-kr/home",
        "https://ccunictf.co.kr/",
        "https://event-us.kr/ubuntukr/event/101263",
        "http://koreaitsecurity.co.kr/landing/summer_camp.asp",
        "https://2025.pycon.kr/",
        "https://aws.amazon.com/ko/events/seminars/aws-techcamp/",
        "https://contest.k-paas.org/",
        "https://aws.amazon.com/ko/events/seminars/aws-techcamp/",
        "https://blog.naver.com/n_cloudplatform/223811699537"
    ]

    os.makedirs("outputs", exist_ok=True)

    for idx, url in enumerate(url_list, start=1):
        file_name = f"outputs/body_cleaned_{idx:02d}.html"
        fetch_clean_body(url, file_name)
