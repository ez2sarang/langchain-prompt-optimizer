#!/bin/bash
# 대화형 모드 테스트 스크립트

echo "대화형 모드를 시작합니다..."
echo "테스트 질의를 자동으로 입력합니다."
echo ""

# 테스트 질의를 자동으로 입력
echo "FastAPI로 REST API 만들기" | python src/main.py --config config/ollama_config.yaml --interactive
