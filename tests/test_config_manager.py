"""
ConfigManager 테스트
"""
import pytest
import tempfile
import os
import yaml

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config_manager import ConfigManager, LLMConfig, OptimizationConfig, DisplayConfig


class TestConfigManager:
    """ConfigManager 테스트 클래스"""
    
    def test_default_config(self):
        """기본 설정 테스트"""
        config_manager = ConfigManager()
        config = config_manager.get_default_config()
        
        assert 'llm' in config
        assert 'optimization' in config
        assert 'display' in config
        assert config['llm']['provider'] == 'ollama'
    
    def test_load_valid_config(self):
        """유효한 설정 파일 로드 테스트"""
        # 임시 설정 파일 생성
        config_data = {
            'llm': {
                'provider': 'ollama',
                'model': 'test-model',
                'base_url': 'http://localhost:11434',
                'temperature': 0.5,
                'max_tokens': 1000
            },
            'optimization': {
                'max_iterations': 2,
                'temperature': 0.5
            },
            'display': {
                'show_timestamps': False,
                'color_output': False
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            llm_config = config_manager.get_llm_config()
            
            assert llm_config.provider == 'ollama'
            assert llm_config.model == 'test-model'
            assert llm_config.temperature == 0.5
        finally:
            os.unlink(temp_path)
    
    def test_validate_config_missing_keys(self):
        """필수 키 누락 설정 검증 테스트"""
        config_manager = ConfigManager()
        
        # llm 키 누락
        invalid_config = {
            'optimization': {},
            'display': {}
        }
        
        assert not config_manager.validate_config(invalid_config)
    
    def test_validate_config_invalid_provider(self):
        """잘못된 provider 검증 테스트"""
        config_manager = ConfigManager()
        
        invalid_config = {
            'llm': {
                'provider': 'invalid_provider',
                'model': 'test',
                'base_url': 'http://localhost:11434'
            }
        }
        
        assert not config_manager.validate_config(invalid_config)
    
    def test_get_llm_config(self):
        """LLM 설정 객체 반환 테스트"""
        config_manager = ConfigManager()
        llm_config = config_manager.get_llm_config()
        
        assert isinstance(llm_config, LLMConfig)
        assert llm_config.provider in ['ollama', 'lmstudio']
        assert llm_config.temperature >= 0 and llm_config.temperature <= 1
    
    def test_get_optimization_config(self):
        """최적화 설정 객체 반환 테스트"""
        config_manager = ConfigManager()
        opt_config = config_manager.get_optimization_config()
        
        assert isinstance(opt_config, OptimizationConfig)
        assert opt_config.max_iterations > 0
    
    def test_get_display_config(self):
        """디스플레이 설정 객체 반환 테스트"""
        config_manager = ConfigManager()
        display_config = config_manager.get_display_config()
        
        assert isinstance(display_config, DisplayConfig)
        assert isinstance(display_config.show_timestamps, bool)
        assert isinstance(display_config.color_output, bool)
    
    def test_load_nonexistent_file(self):
        """존재하지 않는 파일 로드 테스트"""
        config_manager = ConfigManager('nonexistent_file.yaml')
        config = config_manager.config
        
        # 기본 설정이 로드되어야 함
        assert 'llm' in config
        assert config['llm']['provider'] == 'ollama'
