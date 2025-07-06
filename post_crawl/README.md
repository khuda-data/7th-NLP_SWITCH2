# 📅 Post Crawl - 개발자 이벤트 크롤링 & 추천 시스템

> 여러 웹사이트에서 개발자 관련 이벤트, 대회, 강좌 정보를 자동으로 수집하고 AI 기반 추천 시스템을 제공하는 프로젝트입니다.

## 🚀 프로젝트 개요

이 프로젝트는 개발자들이 관심 있어할 만한 이벤트들을 자동으로 수집하고, AI를 활용해 개인화된 추천을 제공합니다.

### 주요 기능
- 📊 **다중 사이트 크롤링**: 4개 주요 사이트에서 이벤트 정보 수집
- 🤖 **AI 기반 분류**: OpenAI API를 사용한 자동 카테고리 분류
- 🎯 **개인화 추천**: 사용자 관심사 기반 이벤트 추천
- 📈 **데이터 전처리**: 날짜 정규화 및 중복 제거
- 💾 **CSV 출력**: 구조화된 데이터로 결과 저장

## 📁 프로젝트 구조

```
post_crawl/
├── 📜 크롤러 파일들
│   ├── dacon_crawler.py          # 데이콘 대회 크롤링
│   ├── devEvent_crawler.py       # 개발자 이벤트 크롤링  
│   ├── inflearn_crawler.py       # 인프런 오프라인 강좌 크롤링
│   └── wevity_crawler.py         # 위비티 이벤트 크롤링
├── 📊 데이터 처리
│   ├── preprocess.ipynb          # 데이터 전처리 및 추천 시스템
│   └── requirements.txt          # 의존성 라이브러리
└── 📋 출력 데이터
    ├── data.csv                  # 크롤링된 원본 데이터
    ├── data_with_desc_dev_category.csv  # AI 분류 결과
    └── recommended_events.csv    # 추천 이벤트 목록
```

## 🛠️ 크롤링 대상 사이트

| 사이트 | 수집 정보 | 특징 |
|--------|-----------|------|
| **데이콘** | 데이터 과학 대회 | 진행 중인 대회만 수집 |
| **개발자 이벤트** | 개발자 컨퍼런스/밋업 | 최신 개발 트렌드 이벤트 |
| **인프런** | 오프라인 강좌 | 모집 중인 강좌만 필터링 |
| **위비티** | 공모전/대회 | 마감되지 않은 이벤트 |

## ⚙️ 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 크롬 드라이버
- webdriver-manager가 자동으로 크롬 드라이버를 설치합니다
- 별도 설치 불필요

## 🎯 사용법

### 1. 개별 크롤러 실행
```bash
# 데이콘 대회 크롤링 (10개 제한)
python dacon_crawler.py

# 개발자 이벤트 크롤링
python devEvent_crawler.py

# 인프런 강좌 크롤링
python inflearn_crawler.py

# 위비티 이벤트 크롤링
python wevity_crawler.py
```

### 2. 통합 데이터 처리
```python
# preprocess.ipynb 실행
jupyter notebook preprocess.ipynb
```

### 3. 추천 시스템 활용
```python
# 관심 키워드 설정
user_keywords = ["백엔드", "클라우드", "AI", "LLM"]

# 유사도 계산
similarity_score = calculate_similarity(user_keywords, event_description)
```

## 🧠 AI 기능

### 1. 자동 카테고리 분류
- **OpenAI GPT-4** 사용
- 5개 카테고리로 분류: 공모전/대회, 부트캠프/교육, 컨퍼런스/포럼, 밋업/네트워킹, 기타
- 개발자 관련 이벤트 필터링

### 2. 개인화 추천
- **SentenceTransformer** 모델 사용
- 다국어 지원: `paraphrase-multilingual-MiniLM-L12-v2`
- 코사인 유사도 기반 매칭

### 3. 데이터 전처리
- 날짜 형식 통일: `YYYY.MM.DD ~ YYYY.MM.DD`
- 주최자 정보 정규화
- 중복 데이터 제거

## 📊 출력 데이터 형식

### 기본 컬럼
- `title`: 이벤트명
- `host`: 주최자
- `date`: 날짜 (정규화됨)
- `url`: 원본 링크

### 추가 컬럼 (AI 처리 후)
- `description`: 이벤트 설명
- `category`: AI 분류 카테고리
- `similarity_score`: 추천 점수

## 🔧 주요 의존성

```
selenium>=4.0.0              # 웹 자동화
beautifulsoup4>=4.9.0        # HTML 파싱
webdriver-manager>=4.0.0     # 드라이버 관리
pandas>=1.3.0                # 데이터 처리
tqdm>=4.62.0                 # 진행률 표시
openai>=1.0.0                # AI 분류
python-dotenv>=0.19.0        # 환경변수 관리
sentence-transformers>=5.0.0 # 유사도 계산
```

## 📈 성능 최적화

### 크롤링 최적화
- **헤드리스 브라우저**: 백그라운드 실행으로 속도 향상
- **지연 시간 조절**: 사이트 부하 방지
- **예외 처리**: 안정적인 데이터 수집

### AI 처리 최적화
- **배치 처리**: 여러 이벤트 동시 분석
- **캐싱**: 이미 분석된 데이터 재사용
- **재시도 로직**: API 호출 실패 시 자동 재시도

## 🚨 주의사항

1. **API 키 필요**: OpenAI API 키가 필요합니다
2. **사용료 발생**: OpenAI API 사용량에 따라 과금됩니다
3. **크롤링 정책**: 각 사이트의 robots.txt 및 이용약관을 준수하세요
4. **속도 제한**: 과도한 요청으로 인한 차단을 방지하세요

## 🔄 업데이트 내역

- **v1.0.0**: 기본 크롤링 기능 구현
- **v1.1.0**: AI 기반 분류 시스템 추가
- **v1.2.0**: 개인화 추천 기능 구현
- **v1.3.0**: 데이터 전처리 로직 개선

## 📞 문의 및 기여

이 프로젝트에 대한 질문이나 개선 제안이 있으시면 언제든지 연락주세요!

---

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!** 