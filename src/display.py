"""
디스플레이 관리 모듈
"""
from datetime import datetime
from typing import Optional
from colorama import Fore, Style, init


# colorama 초기화
init(autoreset=True)


class DisplayManager:
    """최적화 과정 시각화"""
    
    def __init__(self, show_timestamps: bool = True, color_output: bool = True):
        """
        Args:
            show_timestamps: 타임스탬프 표시 여부
            color_output: 색상 출력 사용 여부
        """
        self.show_timestamps = show_timestamps
        self.color_output = color_output
        self.start_time: Optional[datetime] = None
    
    def _get_timestamp(self) -> str:
        """현재 타임스탬프 반환"""
        if not self.show_timestamps:
            return ""
        return f"[{datetime.now().strftime('%H:%M:%S')}] "
    
    def _colorize(self, text: str, color: str) -> str:
        """텍스트에 색상 적용"""
        if not self.color_output:
            return text
        return f"{color}{text}{Style.RESET_ALL}"
    
    def show_header(self):
        """헤더 표시"""
        header = """
╔══════════════════════════════════════════════════════════════╗
║         LangChain Prompt Optimizer                           ║
║         프롬프트 최적화 시스템                                ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(self._colorize(header, Fore.CYAN))
        self.start_time = datetime.now()
    
    def show_original_query(self, query: str):
        """
        원본 질의 표시
        
        Args:
            query: 사용자 질의
        """
        print(f"\n{self._colorize('='*60, Fore.CYAN)}")
        print(self._colorize(f"{self._get_timestamp()}📝 원본 질의", Fore.YELLOW))
        print(self._colorize('='*60, Fore.CYAN))
        print(f"{query}")
        print(self._colorize('='*60, Fore.CYAN))
    
    def show_step(self, step_name: str, description: str, timestamp: Optional[str] = None):
        """
        최적화 단계 표시
        
        Args:
            step_name: 단계 이름
            description: 단계 설명
            timestamp: 타임스탬프 (None이면 현재 시간 사용)
        """
        ts = timestamp if timestamp else self._get_timestamp()
        print(f"\n{self._colorize('─'*60, Fore.BLUE)}")
        print(self._colorize(f"{ts}🔄 {step_name}", Fore.MAGENTA))
        print(self._colorize('─'*60, Fore.BLUE))
        print(f"{description}")
    
    def show_analysis_result(self, analysis: dict):
        """
        분석 결과 표시
        
        Args:
            analysis: 분석 결과 딕셔너리
        """
        print(f"\n{self._colorize('📊 분석 결과:', Fore.CYAN)}")
        for key, value in analysis.items():
            print(f"  • {key}: {value}")
    
    def show_optimized_prompt(self, prompt: str):
        """
        최적화된 프롬프트 표시
        
        Args:
            prompt: 최적화된 프롬프트
        """
        print(f"\n{self._colorize('='*60, Fore.GREEN)}")
        print(self._colorize(f"{self._get_timestamp()}✨ 최적화된 프롬프트", Fore.GREEN))
        print(self._colorize('='*60, Fore.GREEN))
        print(f"{prompt}")
        print(self._colorize('='*60, Fore.GREEN))
    
    def show_llm_response(self, response: str, duration: float):
        """
        LLM 응답 표시
        
        Args:
            response: LLM 응답
            duration: 응답 시간 (초)
        """
        print(f"\n{self._colorize('='*60, Fore.YELLOW)}")
        print(self._colorize(
            f"{self._get_timestamp()}🤖 LLM 응답 (소요 시간: {duration:.2f}초)", 
            Fore.YELLOW
        ))
        print(self._colorize('='*60, Fore.YELLOW))
        print(f"{response}")
        print(self._colorize('='*60, Fore.YELLOW))
    
    def show_error(self, error: Exception, context: str = ""):
        """
        오류 메시지 표시
        
        Args:
            error: 예외 객체
            context: 오류 발생 컨텍스트
        """
        print(f"\n{self._colorize('='*60, Fore.RED)}")
        print(self._colorize(f"{self._get_timestamp()}❌ 오류 발생", Fore.RED))
        if context:
            print(self._colorize(f"컨텍스트: {context}", Fore.RED))
        print(self._colorize('='*60, Fore.RED))
        print(f"{type(error).__name__}: {str(error)}")
        print(self._colorize('='*60, Fore.RED))
    
    def show_info(self, message: str):
        """
        정보 메시지 표시
        
        Args:
            message: 정보 메시지
        """
        print(self._colorize(f"{self._get_timestamp()}ℹ️  {message}", Fore.CYAN))
    
    def show_warning(self, message: str):
        """
        경고 메시지 표시
        
        Args:
            message: 경고 메시지
        """
        print(self._colorize(f"{self._get_timestamp()}⚠️  {message}", Fore.YELLOW))
    
    def show_success(self, message: str):
        """
        성공 메시지 표시
        
        Args:
            message: 성공 메시지
        """
        print(self._colorize(f"{self._get_timestamp()}✅ {message}", Fore.GREEN))
    
    def show_summary(self):
        """전체 실행 요약 표시"""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            print(f"\n{self._colorize('='*60, Fore.CYAN)}")
            print(self._colorize(f"⏱️  전체 소요 시간: {elapsed:.2f}초", Fore.CYAN))
            print(self._colorize('='*60, Fore.CYAN))
    
    def show_provider_info(self, provider_info: dict):
        """
        LLM 제공자 정보 표시
        
        Args:
            provider_info: 제공자 정보 딕셔너리
        """
        print(f"\n{self._colorize('🔧 LLM 설정:', Fore.CYAN)}")
        print(f"  • Provider: {provider_info.get('provider', 'N/A')}")
        print(f"  • Model: {provider_info.get('model', 'N/A')}")
        print(f"  • Base URL: {provider_info.get('base_url', 'N/A')}")
        print(f"  • Temperature: {provider_info.get('temperature', 'N/A')}")
