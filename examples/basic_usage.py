"""
기본 사용 예제

이 스크립트는 LangChain Prompt Optimizer의 기본 사용법을 보여줍니다.
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import PromptOptimizerApp


def example_1_simple_query():
    """예제 1: 간단한 질의"""
    print("\n" + "="*60)
    print("예제 1: 간단한 질의")
    print("="*60)
    
    # 앱 초기화 (Ollama 사용)
    app = PromptOptimizerApp(config_path='config/ollama_config.yaml')
    
    # 질의 실행
    query = "파이썬으로 웹 스크래핑하는 방법"
    result = app.run(query)
    
    if result['success']:
        print("\n✅ 성공!")
        print(f"원본 질의: {result['original_query']}")
        print(f"최적화된 프롬프트: {result['optimized_prompt'][:100]}...")
    else:
        print(f"\n❌ 실패: {result['error']}")


def example_2_technical_query():
    """예제 2: 기술적인 질의"""
    print("\n" + "="*60)
    print("예제 2: 기술적인 질의")
    print("="*60)
    
    # 앱 초기화
    app = PromptOptimizerApp(config_path='config/ollama_config.yaml')
    
    # 더 구체적인 질의
    query = "FastAPI로 REST API 만들기"
    result = app.run(query)
    
    if result['success']:
        print("\n✅ 성공!")


def example_3_lmstudio():
    """예제 3: LM Studio 사용"""
    print("\n" + "="*60)
    print("예제 3: LM Studio 사용")
    print("="*60)
    
    try:
        # LM Studio 설정으로 앱 초기화
        app = PromptOptimizerApp(config_path='config/lmstudio_config.yaml')
        
        # 질의 실행
        query = "머신러닝의 기본 개념 설명"
        result = app.run(query)
        
        if result['success']:
            print("\n✅ 성공!")
    
    except Exception as e:
        print(f"\n⚠️  LM Studio를 사용할 수 없습니다: {e}")
        print("LM Studio가 실행 중인지 확인하세요.")


def example_4_multiple_queries():
    """예제 4: 여러 질의 실행"""
    print("\n" + "="*60)
    print("예제 4: 여러 질의 실행")
    print("="*60)
    
    # 앱 초기화
    app = PromptOptimizerApp(config_path='config/ollama_config.yaml')
    
    # 여러 질의 실행
    queries = [
        "Python 리스트 컴프리헨션",
        "Docker 컨테이너 사용법",
        "Git 브랜치 전략"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- 질의 {i}/{len(queries)} ---")
        result = app.run(query)
        
        if result['success']:
            print(f"✅ '{query}' 처리 완료")
        else:
            print(f"❌ '{query}' 처리 실패: {result['error']}")


def main():
    """메인 함수"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         LangChain Prompt Optimizer - 기본 사용 예제          ║
╚══════════════════════════════════════════════════════════════╝

이 스크립트는 다양한 사용 예제를 보여줍니다.
실행하기 전에 Ollama 또는 LM Studio가 실행 중인지 확인하세요.
""")
    
    try:
        # 예제 1: 간단한 질의
        example_1_simple_query()
        
        # 예제 2: 기술적인 질의
        # example_2_technical_query()
        
        # 예제 3: LM Studio 사용
        # example_3_lmstudio()
        
        # 예제 4: 여러 질의 실행
        # example_4_multiple_queries()
        
        print("\n" + "="*60)
        print("모든 예제 실행 완료!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
