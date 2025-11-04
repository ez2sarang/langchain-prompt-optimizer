## 테스트

```bash
python test_quick.py 2>&1

============================================================
Ollama 연결 테스트
============================================================

설정:
  Provider: ollama
  Model: qwen3-coder:480b-cloud
  Base URL: http://localhost:11434

연결 중...
/Users/ez2sarang/Documents/dev/kiro/langchain/src/llm_provider.py:77: LangChainDeprecationWarning: The class `Ollama` was deprecated in LangCh
ain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the `langchain-ollama package and should be used instead. To use it run `pip install -U `langchain-ollama` and import as `from `langchain_ollama import OllamaLLM``.                                        return Ollama(
✅ 연결 성공!

간단한 질의 테스트...
질의: Hello, how are you? Please respond in one sentence.
응답 대기 중...

응답: Hello! I'm doing well, thank you for asking.

✅ 테스트 완료!
```

## 프롬프트 최적화 시스템을 실행
```bash
python src/main.py --config config/ollama_config.yaml --query "파이썬으로 웹 스크래핑하는 방법" 2>&1

====끝까지 콘솔 출력 내용======

╔══════════════════════════════════════════════════════════════╗
║         LangChain Prompt Optimizer                           ║
║         프롬프트 최적화 시스템                                ║
╚══════════════════════════════════════════════════════════════╝

[23:38:30] ℹ️  LLM 서비스 연결 중...
/Users/ez2sarang/Documents/dev/kiro/langchain/src/llm_provider.py:77: LangChainDeprecationWarning: The class `Ollama` was deprecated in LangCh
ain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the `langchain-ollama package and should be used instead. To use it run `pip install -U `langchain-ollama` and import as `from `langchain_ollama import OllamaLLM``.                                        return Ollama(
[23:38:30] ✅ LLM 서비스 연결 성공!

🔧 LLM 설정:
  • Provider: ollama
  • Model: qwen3-coder:480b-cloud
  • Base URL: http://localhost:11434
  • Temperature: 0.7

============================================================
[23:38:30] 📝 원본 질의
============================================================
파이썬으로 웹 스크래핑하는 방법
============================================================

────────────────────────────────────────────────────────────
[23:38:30] 🔄 1단계: 질의 분석
────────────────────────────────────────────────────────────
사용자 질의의 명확성과 완전성을 분석합니다...

📊 분석 결과:
  • 명확성: 8점 - 주제는 명확하지만 구체적인 목적이나 범위가 약간 모호함
  • 완전성: 6점 - 기본적인 질문은 있으나 구체적인 요구사항이나 조건이 부족함
  • 컨텍스트: 스크래핑할 웹사이트 종류, 사용 목적(데이터 분석, 자동화 등)이 추가되면 좋음

────────────────────────────────────────────────────────────
[23:38:35] 🔄 2단계: 프롬프트 최적화
────────────────────────────────────────────────────────────
분석 결과를 바탕으로 프롬프트를 개선합니다...
[23:38:41] ⚠️  원본 질의의 의도가 일부 변경되었을 수 있습니다.

============================================================
[23:38:41] ✨ 최적화된 프롬프트
============================================================
개선된 프롬프트:

"파이썬을 사용하여 특정 웹사이트(예: 뉴스 사이트, 쇼핑몰 등)에서 데이터를 자동으로 추출하는 웹 스크래핑 프로그램을 만들고 싶습니다. BeautifulS
oup와 requests 라이브러리를 활용한 기본적인 스크래핑 방법과 예제 코드를 제공해주세요. 특히 HTML 파싱, 데이터 추출, 예외 처리 방법을 중점적으로 설명해주시고, 실제 활용 가능한 간단한 예제(예: 뉴스 제목 목록 추출)를 포함해주세요."                                                         ============================================================

────────────────────────────────────────────────────────────
[23:38:41] 🔄 3단계: LLM 호출
────────────────────────────────────────────────────────────
최적화된 프롬프트로 LLM에 질의합니다...

============================================================
[23:39:35] 🤖 LLM 응답 (소요 시간: 53.35초)
============================================================
물론입니다! 아래는 **파이썬을 사용하여 웹 스크래핑 프로그램을 만드는 방법**을 설명하는 개선된 프롬프트에 맞춘 자세한 답변입니다.  
`requests`와 `BeautifulSoup` 라이브러리를 중심으로 **HTML 파싱, 데이터 추출, 예외 처리** 방법을 다루고, **실제 뉴스 제목을 추출하는 예제**를 
포함합니다.                                                                                                                                   
---

## 🌐 웹 스크래핑(Web Scraping)이란?

웹 스크래핑은 웹사이트에서 원하는 정보를 자동으로 추출하는 기술입니다.  
주로 HTML 문서를 파싱하여 필요한 데이터(예: 뉴스 제목, 제품 가격 등)를 가져옵니다.

---

## 🛠 필요한 라이브러리 설치
```
```bash
pip install requests beautifulsoup4
```

- `requests`: 웹사이트에 HTTP 요청을 보내고 HTML 문서를 가져옵니다.
- `BeautifulSoup`: HTML 문서를 파싱하고 원하는 요소를 추출합니다.

---

## 📄 기본적인 웹 스크래핑 예제 (뉴스 제목 추출)

### 예제: 네이버 뉴스 메인 페이지에서 뉴스 제목 추출

```python
import requests
from bs4 import BeautifulSoup

# 1. 웹사이트에 요청 보내기
url = "https://news.naver.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 요청이 실패하면 예외 발생
except requests.exceptions.RequestException as e:
    print(f"요청 오류: {e}")
    exit()

# 2. BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 3. 뉴스 제목 추출 (클래스명은 실제 웹사이트 구조에 따라 다를 수 있음)
# 네이버 뉴스 메인 페이지 구조에 맞는 예시입니다.
news_titles = soup.find_all('a', class_='sa_text_title')

# 4. 제목 출력
for idx, title_tag in enumerate(news_titles, 1):
    title = title_tag.get_text(strip=True)
    link = title_tag['href']
    print(f"{idx}. {title}")
    print(f"링크: {link}\n")
```

---

## 🔍 핵심 개념 설명

### 1. HTML 파싱

- `BeautifulSoup(response.text, 'html.parser')`: HTML 문서를 파싱하여 BeautifulSoup 객체로 변환합니다.
- `'html.parser'`는 파이썬 내장 HTML 파서입니다.

### 2. 데이터 추출

- `soup.find_all()`: 특정 태그와 클래스를 가진 요소를 모두 찾습니다.
- `tag.get_text()`: 태그 내부의 텍스트만 추출합니다.
- `tag['속성명']`: 태그의 속성(예: `href`, `src`)을 가져옵니다.

### 3. 예외 처리

- `requests.exceptions.RequestException`: 요청 실패 시 예외 처리.
- `response.raise_for_status()`: HTTP 에러(404, 500 등) 발생 시 예외를 발생시킵니다.

---

## ⚠️ 주의사항

1. **robots.txt 확인**: 웹사이트의 `robots.txt` 파일을 확인하여 스크래핑이 허용되는지 확인하세요.  
   예: `https://news.naver.com/robots.txt`

2. **과도한 요청 금지**: 너무 빠른 속도로 요청을 보내면 서버에 부하를 줄 수 있습니다. `time.sleep()`을 사용하여 딜레이를 주세요.

3. **사이트 구조 변경**: 웹사이트의 HTML 구조가 수시로 변경될 수 있으므로, 선택자(Selector)도 변경되어야 할 수 있습니다.

---

## ✅ 마무리

이 예제는 웹 스크래핑의 기초를 다루며, 실제 뉴스 제목을 추출하는 간단한 프로그램입니다.  
이를 바탕으로 쇼핑몰 상품 정보, 블로그 포스트, 날씨 정보 등 다양한 데이터를 추출할 수 있습니다.

필요하다면, 특정 사이트에 맞는 선택자나 구조를 분석하여 커스터마이징할 수 있습니다.

---

필요하시면, **특정 쇼핑몰 상품 정보 스크래핑 예제**도 추가로 제공해드릴 수 있습니다!
```bash
============================================================

============================================================
⏱️  전체 소요 시간: 64.57초
============================================================
[23:39:35] ✅ 프롬프트 최적화 완료!

======콘솔 출력 끝=====
```

## 실행 결과 요약
✅ 성공적으로 완료:

Ollama 연결 성공 (qwen3-coder:480b-cloud 모델)

3단계 워크플로우 완료:

질의 분석: 명확성 8점, 완전성 6점으로 평가
프롬프트 최적화: 원본 질의를 구체적이고 상세한 프롬프트로 개선
LLM 호출: 53초 만에 상세한 웹 스크래핑 가이드 생성
전체 소요 시간: 64.57초

결과: BeautifulSoup과 requests를 사용한 완전한 웹 스크래핑 예제 코드와 설명 제공

## 사용 가능한 명령어:
```bash
# 단일 질의 실행
python src/main.py --config config/ollama_config.yaml --query "질의 내용"

# 대화형 모드
python src/main.py --config config/ollama_config.yaml --interactive

# 예제 실행
python examples/basic_usage.py
python examples/custom_optimization.py

# 테스트 실행
pytest tests/
```
