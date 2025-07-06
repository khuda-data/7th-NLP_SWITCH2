import pandas as pd
import webbrowser

# CSV 파일 경로
csv_path = r"C:\Users\seong\OneDrive\Desktop\VSCODE\output\devEvent_competitions_20250706_130506.csv"

# CSV 읽기
df = pd.read_csv(csv_path)

# img_url 컬럼에서 빈 값 제거 후 리스트 생성
img_urls = df["img_url"].dropna().tolist()

# 모든 이미지 URL을 순차적으로 브라우저 탭에서 열기
for url in img_urls:
    webbrowser.open(url)