"""
설정 파일 관리 모듈
"""
import os
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """LLM 설정"""
    provider: str
    model: str
    base_url: str
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class OptimizationConfig:
    """최적화 설정"""
    max_iterations: int = 3
    temperature: float = 0.7


@dataclass
class DisplayConfig:
    """디스플레이 설정"""
    show_timestamps: bool = True
    color_output: bool = True


class ConfigManager:
    """설정 파일 로드 및 검증"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: 설정 파일 경로 (None이면 기본 설정 사용)
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if self.validate_config(config):
                        return config
                    else:
                        print(f"⚠️  설정 파일 검증 실패. 기본 설정을 사용합니다.")
                        return self.get_default_config()
            except Exception as e:
                print(f"⚠️  설정 파일 로드 실패: {e}")
                print("기본 설정을 사용합니다.")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        설정 검증
        
        Args:
            config: 검증할 설정 딕셔너리
            
        Returns:
            검증 성공 여부
        """
        required_keys = ['llm']
        
        # 필수 키 확인
        for key in required_keys:
            if key not in config:
                print(f"❌ 필수 설정 키 누락: {key}")
                return False
        
        # LLM 설정 검증
        llm_config = config.get('llm', {})
        required_llm_keys = ['provider', 'model', 'base_url']
        
        for key in required_llm_keys:
            if key not in llm_config:
                print(f"❌ 필수 LLM 설정 키 누락: {key}")
                return False
        
        # provider 값 검증
        valid_providers = ['ollama', 'lmstudio']
        if llm_config['provider'] not in valid_providers:
            print(f"❌ 지원하지 않는 provider: {llm_config['provider']}")
            print(f"   지원 provider: {', '.join(valid_providers)}")
            return False
        
        return True
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        기본 설정 반환
        
        Returns:
            기본 설정 딕셔너리
        """
        return {
            'llm': {
                'provider': 'ollama',
                'model': 'llama2',
                'base_url': 'http://localhost:11434',
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'optimization': {
                'max_iterations': 3,
                'temperature': 0.7
            },
            'display': {
                'show_timestamps': True,
                'color_output': True
            }
        }
    
    def get_llm_config(self) -> LLMConfig:
        """LLM 설정 객체 반환"""
        llm = self.config.get('llm', {})
        return LLMConfig(
            provider=llm.get('provider', 'ollama'),
            model=llm.get('model', 'llama2'),
            base_url=llm.get('base_url', 'http://localhost:11434'),
            temperature=llm.get('temperature', 0.7),
            max_tokens=llm.get('max_tokens', 2000)
        )
    
    def get_optimization_config(self) -> OptimizationConfig:
        """최적화 설정 객체 반환"""
        opt = self.config.get('optimization', {})
        return OptimizationConfig(
            max_iterations=opt.get('max_iterations', 3),
            temperature=opt.get('temperature', 0.7)
        )
    
    def get_display_config(self) -> DisplayConfig:
        """디스플레이 설정 객체 반환"""
        disp = self.config.get('display', {})
        return DisplayConfig(
            show_timestamps=disp.get('show_timestamps', True),
            color_output=disp.get('color_output', True)
        )
