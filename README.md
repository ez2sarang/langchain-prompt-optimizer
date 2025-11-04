# LangChain Prompt Optimizer

LangChain과 LangGraph를 활용한 프롬프트 최적화 시스템입니다. 사용자의 질의를 로컬 LLM(Ollama, LM Studio)에 전달하기 전에 자동으로 개선하고, 최적화 과정을 실시간으로 시각화합니다.

## 주요 기능

- 🤖 **로컬 LLM 지원**: Ollama와 LM Studio 모두 사용 가능
- 🔄 **자동 프롬프트 최적화**: 질의를 분석하고 개선하여 더 나은 응답 생성
- 📊 **실시간 시각화**: 최적화 과정의 각 단계를 색상과 타임스탬프로 표시
- 🔗 **LangGraph 워크플로우**: 명확한 단계별 처리 구조
- 🔒 **프라이버시 보장**: 모든 처리가 로컬에서 실행

## 데모

```
╔══════════════════════════════════════════════════════════════╗
║         LangChain Prompt Optimizer                           ║
║         프롬프트 최적화 시스템                                ║
╚══════════════════════════════════════════════════════════════╝

[10:30:15] ℹ️  LLM 서비스 연결 중...
[10:30:16] ✅ LLM 서비스 연결 성공!

🔧 LLM 설정:
  • Provider: ollama
  • Model: llama2
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

📊 분석 결과:
  • 명확성: 7/10 - 기본적인 의도는 명확하나 구체성 부족
  • 완전성: 5/10 - 어떤 라이브러리, 어떤 종류의 웹사이트인지 불명확
  • 컨텍스트: BeautifulSoup, Selenium 등 도구 선택 필요

────────────────────────────────────────────────────────────
[10:30:20] 🔄 2단계: 프롬프트 최적화
────────────────────────────────────────────────────────────
분석 결과를 바탕으로 프롬프트를 개선합니다...

============================================================
[10:30:22] ✨ 최적화된 프롬프트
============================================================
Python을 사용하여 웹 스크래핑을 수행하는 방법을 단계별로 설명해주세요.
다음 내용을 포함해주세요:
1. 필요한 라이브러리 (BeautifulSoup, requests 등)
2. 기본적인 HTML 파싱 방법
3. 실제 예제 코드
4. 주의사항 및 베스트 프랙티스
============================================================

────────────────────────────────────────────────────────────
[10:30:23] 🔄 3단계: LLM 호출
────────────────────────────────────────────────────────────
최적화된 프롬프트로 LLM에 질의합니다...

============================================================
[10:30:28] 🤖 LLM 응답 (소요 시간: 5.23초)
============================================================
[LLM의 상세한 응답...]
============================================================

[10:30:28] ✅ 프롬프트 최적화 완료!
============================================================
⏱️  전체 소요 시간: 12.45초
============================================================
```

## 프로젝트 구조

```
langchain-prompt-optimizer/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   ├── ollama_config.yaml
│   └── lmstudio_config.yaml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── llm_provider.py
│   ├── prompt_optimizer.py
│   ├── workflow.py
│   ├── display.py
│   └── config_manager.py
├── examples/
│   ├── basic_usage.py
│   └── custom_optimization.py
└── tests/
    ├── __init__.py
    ├── test_llm_provider.py
    ├── test_optimizer.py
    └── test_workflow.py
```

## 설치 방법

### 1. Python 환경 설정

Python 3.9 이상이 필요합니다.

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 로컬 LLM 설치

#### Ollama 설치

1. [Ollama 공식 사이트](https://ollama.ai)에서 다운로드
2. 설치 후 모델 다운로드:
```bash
ollama pull llama2
# 또는 다른 모델
ollama pull mistral
```

3. Ollama 서비스 실행 (자동으로 실행되지 않는 경우):
```bash
ollama serve
```

#### LM Studio 설치

1. [LM Studio 공식 사이트](https://lmstudio.ai)에서 다운로드
2. 앱 실행 후 원하는 모델 다운로드
3. "Local Server" 탭에서 서버 시작

## 사용 방법

### 기본 사용

```bash
python src/main.py --config config/ollama_config.yaml --query "파이썬으로 웹 스크래핑하는 방법"
```

### 대화형 모드

```bash
python src/main.py --config config/ollama_config.yaml --interactive
```

### LM Studio 사용

```bash
python src/main.py --config config/lmstudio_config.yaml --query "머신러닝 기초 설명"
```

## 설정 파일

### Ollama 설정 예제 (config/ollama_config.yaml)

```yaml
llm:
  provider: "ollama"
  model: "llama2"
  base_url: "http://localhost:11434"
  
optimization:
  max_iterations: 3
  temperature: 0.7
  
display:
  show_timestamps: true
  color_output: true
```

### LM Studio 설정 예제 (config/lmstudio_config.yaml)

```yaml
llm:
  provider: "lmstudio"
  model: "local-model"
  base_url: "http://localhost:1234"
  
optimization:
  max_iterations: 3
  temperature: 0.7
  
display:
  show_timestamps: true
  color_output: true
```

## 예제

### 기본 사용 예제

```python
from src.main import PromptOptimizerApp

app = PromptOptimizerApp(config_path="config/ollama_config.yaml")
result = app.run("파이썬으로 API 만드는 방법")
print(result)
```

더 많은 예제는 `examples/` 디렉토리를 참조하세요.

## 아키텍처

시스템은 LangGraph를 사용한 명확한 워크플로우 구조로 설계되었습니다:

```
사용자 입력
    ↓
[입력 검증]
    ↓
[LangGraph 워크플로우]
    ├─ 질의 분석 노드 (analyze)
    │   └─ 명확성, 완전성, 컨텍스트 평가
    ├─ 프롬프트 최적화 노드 (optimize)
    │   └─ 분석 결과 기반 프롬프트 개선
    └─ LLM 호출 노드 (invoke_llm)
        └─ 최적화된 프롬프트로 응답 생성
    ↓
[결과 표시]
```

### 주요 컴포넌트

1. **ConfigManager**: YAML 설정 파일 로드 및 검증
2. **LLMProviderManager**: Ollama/LM Studio 연결 관리
3. **PromptOptimizer**: 질의 분석 및 프롬프트 최적화
4. **PromptOptimizationWorkflow**: LangGraph 기반 워크플로우
5. **DisplayManager**: 색상 코딩된 실시간 출력

## 문제 해결

### Ollama 연결 오류

**증상**: `LLMConnectionError: ollama 서비스에 연결할 수 없습니다`

**해결 방법**:
1. Ollama가 설치되어 있는지 확인:
   ```bash
   ollama --version
   ```

2. Ollama 서비스 실행:
   ```bash
   ollama serve
   ```

3. 모델이 다운로드되어 있는지 확인:
   ```bash
   ollama list
   ```

4. 모델 다운로드 (필요시):
   ```bash
   ollama pull llama2
   # 또는
   ollama pull mistral
   ```

5. 포트 확인 (기본: 11434):
   ```bash
   curl http://localhost:11434/api/tags
   ```

### LM Studio 연결 오류

**증상**: `LLMConnectionError: lmstudio 서비스에 연결할 수 없습니다`

**해결 방법**:
1. LM Studio 앱이 실행 중인지 확인
2. LM Studio에서 모델을 다운로드하고 로드
3. "Local Server" 탭으로 이동
4. "Start Server" 버튼 클릭
5. 포트 확인 (기본: 1234)
6. 설정 파일의 `base_url`이 올바른지 확인

### 모듈 import 오류

**증상**: `ModuleNotFoundError: No module named 'src'`

**해결 방법**:
```bash
# 프로젝트 루트에서 실행
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 또는 Python 경로를 직접 지정
python -m src.main --query "테스트"
```

### 의존성 오류

**증상**: `ImportError: cannot import name 'X' from 'langchain'`

**해결 방법**:
```bash
# 의존성 재설치
pip install --upgrade -r requirements.txt

# 특정 패키지 업데이트
pip install --upgrade langchain langgraph langchain-community
```

### 느린 응답 시간

**원인**: 로컬 LLM 모델의 크기와 하드웨어 성능에 따라 다름

**개선 방법**:
1. 더 작은 모델 사용 (예: `llama2:7b` 대신 `llama2:3b`)
2. GPU 가속 활성화 (Ollama는 자동으로 GPU 사용)
3. `temperature` 값 조정 (낮을수록 빠름)
4. `max_tokens` 값 감소

### 메모리 부족

**증상**: 시스템이 느려지거나 프로세스가 종료됨

**해결 방법**:
1. 더 작은 모델 사용
2. 다른 애플리케이션 종료
3. Ollama/LM Studio 재시작
4. 시스템 메모리 확인 및 업그레이드 고려

## 개발

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=src

# 특정 테스트 파일
pytest tests/test_workflow.py
```

### 코드 포맷팅

```bash
black src/ tests/
flake8 src/ tests/
```

## 고급 사용법

### 프로그래밍 방식 사용

```python
from src.main import PromptOptimizerApp

# 앱 초기화
app = PromptOptimizerApp(config_path="config/ollama_config.yaml")

# 질의 실행
result = app.run("파이썬으로 API 만드는 방법")

if result['success']:
    print(f"원본: {result['original_query']}")
    print(f"최적화: {result['optimized_prompt']}")
    print(f"응답: {result['llm_response']}")
```

### 커스텀 설정

```python
from src.config_manager import ConfigManager
from src.llm_provider import LLMProviderManager
from src.prompt_optimizer import PromptOptimizer
from src.workflow import PromptOptimizationWorkflow
from src.display import DisplayManager

# 커스텀 설정
custom_config = {
    'llm': {
        'provider': 'ollama',
        'model': 'mistral',
        'base_url': 'http://localhost:11434',
        'temperature': 0.5,
        'max_tokens': 1000
    }
}

# 컴포넌트 초기화
config_manager = ConfigManager()
config_manager.config = custom_config

llm_config = config_manager.get_llm_config()
llm_provider = LLMProviderManager(
    provider=llm_config.provider,
    model=llm_config.model,
    base_url=llm_config.base_url
)

prompt_optimizer = PromptOptimizer(llm_provider)
display = DisplayManager()
workflow = PromptOptimizationWorkflow(llm_provider, prompt_optimizer, display)

# 실행
final_state = workflow.run("질의 내용")
```

### 배치 처리

```python
app = PromptOptimizerApp(config_path="config/ollama_config.yaml")

queries = [
    "React 컴포넌트 설계",
    "SQL 쿼리 최적화",
    "마이크로서비스 아키텍처"
]

results = []
for query in queries:
    result = app.run(query)
    results.append(result)
    
    # 다음 질의 전에 히스토리 초기화
    app.workflow.clear_history()
    app.prompt_optimizer.clear_steps()
```

## 성능 최적화 팁

1. **모델 선택**: 작업에 적합한 크기의 모델 선택
   - 간단한 질의: `llama2:7b`, `mistral:7b`
   - 복잡한 질의: `llama2:13b`, `mixtral:8x7b`

2. **Temperature 조정**: 
   - 결정적 출력: `0.1-0.3`
   - 창의적 출력: `0.7-0.9`

3. **캐싱**: 동일한 질의는 결과를 캐싱하여 재사용

4. **병렬 처리**: 여러 질의를 동시에 처리 (주의: 메모리 사용량 증가)

## 확장 가능성

이 프로젝트는 다음과 같이 확장할 수 있습니다:

- **추가 LLM 제공자**: OpenAI, Anthropic, HuggingFace 등
- **RAG 통합**: 벡터 데이터베이스를 사용한 컨텍스트 검색
- **웹 인터페이스**: Streamlit 또는 Gradio UI
- **프롬프트 템플릿**: 도메인별 최적화 전략
- **평가 메트릭**: 최적화 품질 측정
- **로깅 및 모니터링**: 성능 추적 및 분석

## 기여 가이드

기여를 환영합니다! 다음 단계를 따라주세요:

1. 이 저장소를 Fork
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

### 개발 가이드라인

- 코드 스타일: Black 포맷터 사용
- 린팅: Flake8
- 테스트: pytest로 테스트 작성
- 문서화: 모든 함수에 docstring 추가

## 제작자

**Jeong Jaewoo**
- GitHub: [@ez2sarang](https://github.com/ez2sarang)

## 비즈니스 문의

프로젝트 관련 비즈니스 문의는 아래 이메일로 연락주세요:
- 📧 **sales@com.dooray.com**

## 참고 자료

- [LangChain 문서](https://python.langchain.com/)
- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [Ollama 문서](https://ollama.ai/docs)
- [LM Studio](https://lmstudio.ai/)

## 문의

- 기술적 질문이나 이슈: [GitHub Issues](https://github.com/ez2sarang/langchain-prompt-optimizer/issues)
- 비즈니스 문의: sales@com.dooray.com
