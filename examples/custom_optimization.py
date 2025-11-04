"""
고급 사용 예제 - 커스텀 최적화

이 스크립트는 프롬프트 최적화 시스템의 고급 기능을 보여줍니다.
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config_manager import ConfigManager
from src.llm_provider import LLMProviderManager
from src.prompt_optimizer import PromptOptimizer
from src.workflow import PromptOptimizationWorkflow
from src.display import DisplayManager


def example_1_custom_config():
    """예제 1: 커스텀 설정 사용"""
    print("\n" + "="*60)
    print("예제 1: 커스텀 설정 사용")
    print("="*60)
    
    # 커스텀 설정 생성
    custom_config = {
        'llm': {
            'provider': 'ollama',
            'model': 'mistral',  # 다른 모델 사용
            'base_url': 'http://localhost:11434',
            'temperature': 0.5,  # 더 결정적인 출력
            'max_tokens': 1000
        },
        'optimization': {
            'max_iterations': 2,
            'temperature': 0.5
        },
        'display': {
            'show_timestamps': True,
            'color_output': True
        }
    }
    
    # 설정 매니저 초기화
    config_manager = ConfigManager()
    config_manager.config = custom_config
    
    # 컴포넌트 초기화
    llm_config = config_manager.get_llm_config()
    display_config = config_manager.get_display_config()
    
    display = DisplayManager(
        show_timestamps=display_config.show_timestamps,
        color_output=display_config.color_output
    )
    
    display.show_header()
    display.show_info(f"커스텀 모델 사용: {llm_config.model}")
    
    try:
        llm_provider = LLMProviderManager(
            provider=llm_config.provider,
            model=llm_config.model,
            base_url=llm_config.base_url,
            temperature=llm_config.temperature,
            max_tokens=llm_config.max_tokens
        )
        
        prompt_optimizer = PromptOptimizer(llm_provider)
        workflow = PromptOptimizationWorkflow(llm_provider, prompt_optimizer, display)
        
        # 질의 실행
        query = "딥러닝과 머신러닝의 차이"
        final_state = workflow.run(query)
        
        if not final_state.get('error'):
            display.show_success("커스텀 설정으로 실행 완료!")
    
    except Exception as e:
        display.show_error(e, "커스텀 설정 실행")


def example_2_analyze_optimization_steps():
    """예제 2: 최적화 단계 분석"""
    print("\n" + "="*60)
    print("예제 2: 최적화 단계 분석")
    print("="*60)
    
    # 기본 설정으로 초기화
    config_manager = ConfigManager('config/ollama_config.yaml')
    llm_config = config_manager.get_llm_config()
    display_config = config_manager.get_display_config()
    
    display = DisplayManager(
        show_timestamps=display_config.show_timestamps,
        color_output=display_config.color_output
    )
    
    display.show_header()
    
    try:
        llm_provider = LLMProviderManager(
            provider=llm_config.provider,
            model=llm_config.model,
            base_url=llm_config.base_url,
            temperature=llm_config.temperature,
            max_tokens=llm_config.max_tokens
        )
        
        prompt_optimizer = PromptOptimizer(llm_provider)
        workflow = PromptOptimizationWorkflow(llm_provider, prompt_optimizer, display)
        
        # 질의 실행
        query = "API 설계 베스트 프랙티스"
        final_state = workflow.run(query)
        
        # 최적화 단계 분석
        print("\n" + "="*60)
        print("최적화 단계 상세 분석")
        print("="*60)
        
        steps = prompt_optimizer.get_optimization_steps()
        for i, step in enumerate(steps, 1):
            print(f"\n단계 {i}: {step.name}")
            print(f"  시간: {step.timestamp.strftime('%H:%M:%S')}")
            print(f"  설명: {step.description}")
            print(f"  입력 길이: {len(step.input_data)} 문자")
            print(f"  출력 길이: {len(step.output_data)} 문자")
        
        # 상태 히스토리 분석
        print("\n" + "="*60)
        print("워크플로우 상태 히스토리")
        print("="*60)
        
        history = workflow.get_state_history()
        for i, state in enumerate(history, 1):
            print(f"\n상태 {i}:")
            print(f"  완료된 단계: {len(state['steps'])}")
            if state['steps']:
                last_step = state['steps'][-1]
                print(f"  마지막 단계: {last_step['name']}")
                print(f"  상태: {last_step['status']}")
    
    except Exception as e:
        display.show_error(e, "단계 분석")


def example_3_intent_preservation_check():
    """예제 3: 의도 보존 검증"""
    print("\n" + "="*60)
    print("예제 3: 의도 보존 검증")
    print("="*60)
    
    config_manager = ConfigManager('config/ollama_config.yaml')
    llm_config = config_manager.get_llm_config()
    
    display = DisplayManager()
    display.show_header()
    
    try:
        llm_provider = LLMProviderManager(
            provider=llm_config.provider,
            model=llm_config.model,
            base_url=llm_config.base_url,
            temperature=llm_config.temperature,
            max_tokens=llm_config.max_tokens
        )
        
        prompt_optimizer = PromptOptimizer(llm_provider)
        
        # 여러 질의로 의도 보존 테스트
        test_queries = [
            "Python 배우기",
            "데이터베이스 최적화 방법",
            "클라우드 컴퓨팅이란?"
        ]
        
        for query in test_queries:
            print(f"\n--- 테스트: '{query}' ---")
            
            # 분석 및 최적화
            analysis = prompt_optimizer.analyze_query(query)
            optimized = prompt_optimizer.optimize_prompt(query, analysis)
            
            # 의도 보존 검증
            preserved = prompt_optimizer.check_intent_preservation(query, optimized)
            
            print(f"원본: {query}")
            print(f"최적화: {optimized[:100]}...")
            print(f"의도 보존: {'✅ 예' if preserved else '❌ 아니오'}")
    
    except Exception as e:
        display.show_error(e, "의도 보존 검증")


def example_4_batch_processing():
    """예제 4: 배치 처리"""
    print("\n" + "="*60)
    print("예제 4: 배치 처리")
    print("="*60)
    
    config_manager = ConfigManager('config/ollama_config.yaml')
    llm_config = config_manager.get_llm_config()
    display_config = config_manager.get_display_config()
    
    display = DisplayManager(
        show_timestamps=display_config.show_timestamps,
        color_output=display_config.color_output
    )
    
    display.show_header()
    
    try:
        llm_provider = LLMProviderManager(
            provider=llm_config.provider,
            model=llm_config.model,
            base_url=llm_config.base_url,
            temperature=llm_config.temperature,
            max_tokens=llm_config.max_tokens
        )
        
        prompt_optimizer = PromptOptimizer(llm_provider)
        workflow = PromptOptimizationWorkflow(llm_provider, prompt_optimizer, display)
        
        # 배치 질의
        queries = [
            "React 컴포넌트 설계",
            "SQL 쿼리 최적화",
            "마이크로서비스 아키텍처"
        ]
        
        results = []
        
        for i, query in enumerate(queries, 1):
            display.show_info(f"배치 처리 {i}/{len(queries)}")
            
            final_state = workflow.run(query)
            
            results.append({
                'query': query,
                'success': not final_state.get('error'),
                'optimized': final_state.get('optimized_prompt', ''),
                'response': final_state.get('llm_response', '')
            })
            
            # 다음 질의 전에 히스토리 초기화
            workflow.clear_history()
            prompt_optimizer.clear_steps()
        
        # 결과 요약
        print("\n" + "="*60)
        print("배치 처리 결과 요약")
        print("="*60)
        
        for i, result in enumerate(results, 1):
            status = "✅ 성공" if result['success'] else "❌ 실패"
            print(f"\n{i}. {result['query']}")
            print(f"   상태: {status}")
            if result['success']:
                print(f"   최적화 길이: {len(result['optimized'])} 문자")
                print(f"   응답 길이: {len(result['response'])} 문자")
    
    except Exception as e:
        display.show_error(e, "배치 처리")


def main():
    """메인 함수"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║      LangChain Prompt Optimizer - 고급 사용 예제             ║
╚══════════════════════════════════════════════════════════════╝

이 스크립트는 고급 기능과 커스터마이징 방법을 보여줍니다.
""")
    
    try:
        # 예제 1: 커스텀 설정
        # example_1_custom_config()
        
        # 예제 2: 최적화 단계 분석
        example_2_analyze_optimization_steps()
        
        # 예제 3: 의도 보존 검증
        # example_3_intent_preservation_check()
        
        # 예제 4: 배치 처리
        # example_4_batch_processing()
        
        print("\n" + "="*60)
        print("고급 예제 실행 완료!")
        print("="*60)
    
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
