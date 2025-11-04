# 빠른 시작 가이드

이 가이드는 LangChain Prompt Optimizer를 5분 안에 시작하는 방법을 안내합니다.

## 전제 조건

- Python 3.9 이상
- Ollama 또는 LM Studio 설치

## 1단계: 프로젝트 클론

```bash
git clone https://github.com/ez2sarang/langchain-prompt-optimizer.git
cd langchain-prompt-optimizer
```

## 2단계: 의존성 설치

```bash
# Python 3.12 사용 권장
python -m pip install langchain langchain-community langgraph colorama pyyaml python-dotenv requests
```

또는 requirements.txt 사용:

```bash
python -m pip install -r requirements.txt
```

## 3단계: Ollama 설정

### Ollama 설치 (아직 설치하지 않은 경우)

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
[Ollama 공식 사이트](https://ollama.ai)에서 다운로드

### 모델 다운로드

```bash
# 추천 모델 (빠르고 효율적)
ollama pull gemma2:2b

# 또는 다른 모델
ollama pull llama2
ollama pull mistral
```

### Ollama 서비스 시작

```bash
ollama serve
```

## 4단계: 설정 파일 수정

`config/ollama_config.yaml` 파일을 열고 모델 이름을 확인:

```yaml
llm:
  provider: "ollama"
  model: "gemma2:2b"  # 다운로드한 모델 이름
  base_url: "http://localhost:11434"
  temperature: 0.7
  max_tokens: 2000
```

## 5단계: 실행!

### 단일 질의 실행

```bash
python src/main.py --config config/ollama_config.yaml --query "파이썬으로 웹 스크래핑하는 방법"
```

### 대화형 모드

```bash
python src/main.py --config config/ollama_config.yaml --interactive
```

## 예상 출력

```
╔══════════════════════════════════════════════════════════════╗
║         LangChain Prompt Optimizer                           ║
║         프롬프트 최적화 시스템                                ║
╚══════════════════════════════════════════════════════════════╝

[10:30:15] ℹ️  LLM 서비스 연결 중...
[10:30:16] ✅ LLM 서비스 연결 성공!

🔧 LLM 설정:
  • Provider: ollama
  • Model: gemma2:2b
  • Base URL: http://localhost:11434

============================================================
[10:30:16] 📝 원본 질의
============================================================
파이썬으로 웹 스크래핑하는 방법
============================================================

────────────────────────────────────────────────────────────
[10:30:17] 🔄 1단계: 질의 분석
────────────────────────────────────────────────────────────
사용자 질의의 명확성과 완전성을 분석합니다...

[... 최적화 과정 ...]

✅ 프롬프트 최적화 완료!
```

## 문제 해결

### Ollama 연결 오류

```bash
# Ollama가 실행 중인지 확인
curl http://localhost:11434/api/tags

# 모델 목록 확인
ollama list
```

### 모듈 import 오류

```bash
# Python 버전 확인
python --version

# pip 버전 확인
python -m pip --version

# 의존성 재설치
python -m pip install --upgrade -r requirements.txt
```

### 느린 응답

- 더 작은 모델 사용 (gemma2:2b 권장)
- `max_tokens` 값을 줄이기 (config 파일에서)
- GPU가 있다면 Ollama가 자동으로 사용합니다

## 다음 단계

- 📖 [전체 문서 읽기](README.md)
- 🔧 [고급 설정 및 커스터마이징](examples/custom_optimization.py)
- 🧪 [테스트 실행](tests/)
- 💡 [예제 탐색](examples/)

## 도움이 필요하신가요?

- 기술 문의: [GitHub Issues](https://github.com/ez2sarang/langchain-prompt-optimizer/issues)
- 비즈니스 문의: sales@com.dooray.com

---

**즐거운 코딩 되세요! 🚀**
