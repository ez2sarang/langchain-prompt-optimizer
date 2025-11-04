"""
LLM Provider 관리 모듈
"""
import requests
from typing import Optional, Any
from langchain_community.llms import Ollama


class LLMConnectionError(Exception):
    """LLM 연결 오류"""
    pass


class LLMProviderManager:
    """로컬 LLM 제공자 관리"""
    
    def __init__(self, provider: str, model: str, base_url: str, 
                 temperature: float = 0.7, max_tokens: int = 2000):
        """
        Args:
            provider: LLM 제공자 ('ollama' 또는 'lmstudio')
            model: 모델 이름
            base_url: LLM 서비스 URL
            temperature: 생성 temperature
            max_tokens: 최대 토큰 수
        """
        self.provider = provider.lower()
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm: Optional[Any] = None
        
        # 연결 검증
        if not self.validate_connection():
            raise LLMConnectionError(
                f"{self.provider} 서비스에 연결할 수 없습니다. "
                f"서비스가 실행 중인지 확인하세요: {self.base_url}"
            )
        
        # LLM 초기화
        self.llm = self._initialize_llm()
    
    def validate_connection(self) -> bool:
        """
        LLM 서비스 연결 검증
        
        Returns:
            연결 성공 여부
        """
        try:
            if self.provider == 'ollama':
                # Ollama health check
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
                return response.status_code == 200
            
            elif self.provider == 'lmstudio':
                # LM Studio health check
                response = requests.get(f"{self.base_url}/v1/models", timeout=5)
                return response.status_code == 200
            
            else:
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 연결 오류: {e}")
            return False
    
    def _initialize_llm(self) -> Any:
        """
        LLM 객체 초기화
        
        Returns:
            초기화된 LLM 객체
        """
        if self.provider == 'ollama':
            return Ollama(
                model=self.model,
                base_url=self.base_url,
                temperature=self.temperature,
            )
        
        elif self.provider == 'lmstudio':
            # LM Studio는 OpenAI 호환 API 사용
            from langchain_community.llms import OpenAI
            return OpenAI(
                model=self.model,
                base_url=f"{self.base_url}/v1",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key="lm-studio"  # LM Studio는 더미 키 필요
            )
        
        else:
            raise ValueError(f"지원하지 않는 provider: {self.provider}")
    
    def get_llm(self) -> Any:
        """
        LLM 객체 반환
        
        Returns:
            LLM 객체
        """
        if self.llm is None:
            raise LLMConnectionError("LLM이 초기화되지 않았습니다.")
        return self.llm
    
    def invoke(self, prompt: str, retry_count: int = 3) -> str:
        """
        LLM 호출
        
        Args:
            prompt: 입력 프롬프트
            retry_count: 재시도 횟수
            
        Returns:
            LLM 응답
        """
        if self.llm is None:
            raise LLMConnectionError("LLM이 초기화되지 않았습니다.")
        
        for attempt in range(retry_count):
            try:
                response = self.llm.invoke(prompt)
                return response
            
            except Exception as e:
                if attempt < retry_count - 1:
                    print(f"⚠️  LLM 호출 실패 (시도 {attempt + 1}/{retry_count}): {e}")
                    print("재시도 중...")
                else:
                    raise LLMConnectionError(
                        f"LLM 호출 실패 ({retry_count}회 시도): {e}"
                    )
        
        return ""
    
    def get_provider_info(self) -> dict:
        """
        제공자 정보 반환
        
        Returns:
            제공자 정보 딕셔너리
        """
        return {
            'provider': self.provider,
            'model': self.model,
            'base_url': self.base_url,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
