# 🕷️ Event Crawling Project

대한민국의 주요 개발자/AI 관련 이벤트, 공모전, 대회 정보를 수집하는 크롤링 프로젝트입니다.

## 📋 프로젝트 개요

이 프로젝트는 다음 세 개 사이트에서 이벤트 정보를 자동으로 수집합니다:
- **위비티(Wevity)**: 각종 공모전 및 대외활동
- **데이콘(Dacon)**: AI/데이터 사이언스 경진대회
- **개발자 이벤트**: 개발자 관련 세미나, 컨퍼런스, 워크샵

## 🗂️ 파일 구조

### 🕷️ 크롤러 파일들
- `wevity_crawler.py` - 위비티 공모전 크롤링
- `dacon_crawler.py` - 데이콘 AI 대회 크롤링  
- `devEvent_crawler.py` - 개발자 이벤트 크롤링

### 📊 데이터 처리
- `preprocess.ipynb` - 수집된 데이터 통합 및 전처리

### 🗂️ 기타 파일들
- `dacon_crawling.ipynb` - 데이콘 크롤링 개발/테스트용 노트북
- `get_devEventHTML.py` - HTML 파싱 유틸리티
- `wevity_detail_html.py` - 위비티 상세 페이지 HTML 처리
- 기타 개발 과정 파일들

## 🚀 사용법

### 1. 환경 설정

필요한 패키지를 설치합니다:

```bash
pip install selenium webdriver-manager pandas playwright beautifulsoup4
```

Playwright 브라우저 설치:
```bash
playwright install chromium
```

### 2. 개별 크롤러 실행

각 크롤러를 단독으로 실행할 수 있습니다:

```bash
# 위비티 크롤링
python wevity_crawler.py

# 데이콘 크롤링  
python dacon_crawler.py

# 개발자 이벤트 크롤링
python devEvent_crawler.py
```

실행 결과는 `output/` 폴더에 타임스탬프가 포함된 CSV 파일로 저장됩니다.

### 3. 통합 데이터 처리

Jupyter Notebook에서 `preprocess.ipynb`를 실행하여:
- 세 사이트의 데이터를 통합
- 날짜 형식 통일 (`YYYY.MM.DD ~ YYYY.MM.DD`)
- HTML에서 텍스트 추출
- 최종 `data.csv` 파일 생성

```python
# Jupyter Notebook에서 실행
from wevity_crawler import crawl_wevity
from dacon_crawler import crawl_dacon  
from devEvent_crawler import crawl_devEvent

# 데이터 수집
df_wevity = crawl_wevity()
df_dacon = await crawl_dacon()  # 비동기
df_dev = await crawl_devEvent()  # 비동기

# 나머지 전처리는 노트북 참조
```

## 📊 수집되는 데이터

각 크롤러는 다음 정보를 수집합니다:

| 컬럼 | 설명 | 예시 |
|------|------|------|
| `title` | 이벤트/대회 제목 | "Jump AI 2025 : 제 3회 AI 신약개발 경진대회" |
| `date` | 기간 (통일된 형식) | "2025.07.07 ~ 2025.08.25" |
| `host` | 주최기관 | "한국제약바이오협회" |
| `url` | 원본 링크 | "https://dacon.io/competitions/..." |
| `description` | 이벤트 설명 (HTML → 텍스트) | "AI를 활용한 신약개발..." |

## 🔧 크롤러별 특징

### 위비티 크롤러 (`wevity_crawler.py`)
- **기술**: Selenium + BeautifulSoup
- **특징**: D-day 기반 필터링, 상세 페이지 HTML 수집
- **수집 대상**: 공모전, 대외활동, 인턴십

### 데이콘 크롤러 (`dacon_crawler.py`)
- **기술**: Selenium + Playwright + BeautifulSoup  
- **특징**: 마감된 대회 자동 제외, `div.ql-editor` 영역만 추출
- **수집 대상**: AI/ML 경진대회, 해커톤

### 개발자 이벤트 크롤러 (`devEvent_crawler.py`)
- **기술**: Selenium + Playwright + BeautifulSoup
- **특징**: 비동기 HTML 파싱
- **수집 대상**: 개발자 세미나, 컨퍼런스, 워크샵

## 📁 출력 파일

### 개별 크롤러 출력
```
output/
├── wevity_events_20250107_143022.csv
├── dacon_competitions_20250107_143145.csv
└── devEvent_events_20250107_143301.csv
```

### 통합 전처리 출력
```
data.csv  # 최종 통합 데이터
```

## ⚙️ 설정 옵션

### 데이콘 크롤러 제한
`dacon_crawler.py`에서 크롤링할 대회 수를 제한할 수 있습니다:

```python
# 전체 크롤링
df = await crawl_dacon()

# 최신 20개만 크롤링
df = await crawl_dacon(limit=20)
```

### 브라우저 옵션
모든 크롤러는 headless 모드로 실행됩니다. 디버깅 시에는 각 파일에서 `--headless` 옵션을 제거하세요.

## 🛠️ 트러블슈팅

### 1. ChromeDriver 오류
```bash
# ChromeDriver 재설치
brew install chromedriver
```

### 2. Playwright 오류  
```bash
# Playwright 재설치
playwright install
```

### 3. 메모리 부족
큰 데이터셋 처리 시 limit 옵션을 사용하여 단계별로 수집하세요.

## 📝 주의사항

- 크롤링 간격을 적절히 설정하여 서버에 부하를 주지 않도록 주의
- 사이트 구조 변경 시 셀렉터 수정이 필요할 수 있음
- 개인적 용도로만 사용하고, 상업적 이용 시 해당 사이트 이용약관 확인 필요

## 🔄 업데이트

사이트 구조가 변경되면 다음 파일들을 업데이트해야 할 수 있습니다:
- CSS 셀렉터
- 정규표현식 패턴  
- HTML 파싱 로직

---

**Happy Crawling! 🕷️✨** 