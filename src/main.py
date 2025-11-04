"""
메인 애플리케이션
"""
import argparse
import sys
from typing import Optional

from config_manager import ConfigManager
from llm_provider import LLMProviderManager, LLMConnectionError
from prompt_optimizer import PromptOptimizer, OptimizationError
from workflow import PromptOptimizationWorkflow
from display import DisplayManager


class PromptOptimizerApp:
    """프롬프트 최적화 애플리케이션"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: 설정 파일 경로
        """
        # 설정 로드
        self.config_manager = ConfigManager(config_path)
        llm_config = self.config_manager.get_llm_config()
        display_config = self.config_manager.get_display_config()
        
        # 디스플레이 매니저 초기화
        self.display = DisplayManager(
            show_timestamps=display_config.show_timestamps,
            color_output=display_config.color_output
        )
        
        # 헤더 표시
        self.display.show_header()
        
        try:
            # LLM Provider 초기화
            self.display.show_info("LLM 서비스 연결 중...")
            self.llm_provider = LLMProviderManager(
                provider=llm_config.provider,
                model=llm_config.model,
                base_url=llm_config.base_url,
                temperature=llm_config.temperature,
                max_tokens=llm_config.max_tokens
            )
            self.display.show_success("LLM 서비스 연결 성공!")
            self.display.show_provider_info(self.llm_provider.get_provider_info())
            
        except LLMConnectionError as e:
            self.display.show_error(e, "LLM 초기화")
            self._show_connection_help(llm_config.provider)
            sys.exit(1)
        
        # Prompt Optimizer 초기화
        self.prompt_optimizer = PromptOptimizer(self.llm_provider)
        
        # Workflow 초기화
        self.workflow = PromptOptimizationWorkflow(
            self.llm_provider,
            self.prompt_optimizer,
            self.display
        )
    
    def _show_connection_help(self, provider: str):
        """
        연결 도움말 표시
        
        Args:
            provider: LLM 제공자
        """
        if provider == 'ollama':
            print("\n💡 Ollama 연결 문제 해결:")
            print("   1. Ollama가 설치되어 있는지 확인: https://ollama.ai")
            print("   2. Ollama 서비스 실행: ollama serve")
            print("   3. 모델 다운로드: ollama pull llama2")
            print("   4. 포트 확인: 기본 포트는 11434")
        
        elif provider == 'lmstudio':
            print("\n💡 LM Studio 연결 문제 해결:")
            print("   1. LM Studio가 설치되어 있는지 확인: https://lmstudio.ai")
            print("   2. LM Studio 실행 후 모델 다운로드")
            print("   3. 'Local Server' 탭에서 서버 시작")
            print("   4. 포트 확인: 기본 포트는 1234")
    
    def run(self, query: str) -> dict:
        """
        질의 실행
        
        Args:
            query: 사용자 질의
            
        Returns:
            실행 결과
        """
        try:
            # 워크플로우 실행
            final_state = self.workflow.run(query)
            
            # 요약 표시
            self.display.show_summary()
            
            # 오류 확인
            if final_state.get('error'):
                self.display.show_error(
                    Exception(final_state['error']),
                    "워크플로우 실행"
                )
                return {'success': False, 'error': final_state['error']}
            
            self.display.show_success("프롬프트 최적화 완료!")
            
            return {
                'success': True,
                'original_query': final_state['original_query'],
                'optimized_prompt': final_state['optimized_prompt'],
                'llm_response': final_state['llm_response'],
                'analysis': final_state['analysis'],
                'timestamps': final_state['timestamps']
            }
            
        except OptimizationError as e:
            self.display.show_error(e, "최적화")
            return {'success': False, 'error': str(e)}
        
        except Exception as e:
            self.display.show_error(e, "실행")
            return {'success': False, 'error': str(e)}
    
    def run_interactive(self):
        """대화형 모드 실행"""
        self.display.show_info("대화형 모드 시작 (종료: 'quit' 또는 'exit')")
        
        while True:
            try:
                # 사용자 입력
                print(f"\n{'-'*60}")
                query = input("질의를 입력하세요: ").strip()
                
                # 종료 확인
                if query.lower() in ['quit', 'exit', '종료']:
                    self.display.show_info("프로그램을 종료합니다.")
                    break
                
                # 빈 입력 확인
                if not query:
                    self.display.show_warning("질의를 입력해주세요.")
                    continue
                
                # 질의 실행
                self.run(query)
                
            except KeyboardInterrupt:
                print("\n")
                self.display.show_info("프로그램을 종료합니다.")
                break
            
            except Exception as e:
                self.display.show_error(e, "대화형 모드")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='LangChain Prompt Optimizer - 프롬프트 최적화 시스템'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/ollama_config.yaml',
        help='설정 파일 경로 (기본: config/ollama_config.yaml)'
    )
    
    parser.add_argument(
        '--query',
        type=str,
        help='실행할 질의'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='대화형 모드 실행'
    )
    
    args = parser.parse_args()
    
    try:
        # 앱 초기화
        app = PromptOptimizerApp(config_path=args.config)
        
        # 실행 모드 결정
        if args.interactive:
            # 대화형 모드
            app.run_interactive()
        
        elif args.query:
            # 단일 질의 모드
            app.run(args.query)
        
        else:
            # 인자가 없으면 도움말 표시
            parser.print_help()
            print("\n예제:")
            print("  python src/main.py --query '파이썬으로 웹 스크래핑하는 방법'")
            print("  python src/main.py --interactive")
            print("  python src/main.py --config config/lmstudio_config.yaml --query '머신러닝 기초'")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
