"""
LLMProviderManager 테스트
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm_provider import LLMProviderManager, LLMConnectionError


class TestLLMProviderManager:
    """LLMProviderManager 테스트 클래스"""
    
    @patch('src.llm_provider.requests.get')
    def test_validate_connection_ollama_success(self, mock_get):
        """Ollama 연결 검증 성공 테스트"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # LLMProviderManager 초기화 시도
        with patch('src.llm_provider.LLMProviderManager._initialize_llm'):
            provider = LLMProviderManager(
                provider='ollama',
                model='test-model',
                base_url='http://localhost:11434'
            )
            
            assert provider.validate_connection() == True
    
    @patch('src.llm_provider.requests.get')
    def test_validate_connection_ollama_failure(self, mock_get):
        """Ollama 연결 검증 실패 테스트"""
        # Mock 응답 설정 (연결 실패)
        mock_get.side_effect = Exception("Connection failed")
        
        # 연결 실패 시 예외 발생 확인
        with pytest.raises(LLMConnectionError):
            LLMProviderManager(
                provider='ollama',
                model='test-model',
                base_url='http://localhost:11434'
            )
    
    @patch('src.llm_provider.requests.get')
    def test_validate_connection_lmstudio_success(self, mock_get):
        """LM Studio 연결 검증 성공 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with patch('src.llm_provider.LLMProviderManager._initialize_llm'):
            provider = LLMProviderManager(
                provider='lmstudio',
                model='test-model',
                base_url='http://localhost:1234'
            )
            
            assert provider.validate_connection() == True
    
    @patch('src.llm_provider.requests.get')
    @patch('src.llm_provider.Ollama')
    def test_initialize_llm_ollama(self, mock_ollama, mock_get):
        """Ollama LLM 초기화 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        mock_llm = Mock()
        mock_ollama.return_value = mock_llm
        
        provider = LLMProviderManager(
            provider='ollama',
            model='test-model',
            base_url='http://localhost:11434',
            temperature=0.7
        )
        
        assert provider.llm is not None
        mock_ollama.assert_called_once()
    
    @patch('src.llm_provider.requests.get')
    def test_get_provider_info(self, mock_get):
        """제공자 정보 반환 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with patch('src.llm_provider.LLMProviderManager._initialize_llm'):
            provider = LLMProviderManager(
                provider='ollama',
                model='test-model',
                base_url='http://localhost:11434',
                temperature=0.5,
                max_tokens=1000
            )
            
            info = provider.get_provider_info()
            
            assert info['provider'] == 'ollama'
            assert info['model'] == 'test-model'
            assert info['base_url'] == 'http://localhost:11434'
            assert info['temperature'] == 0.5
            assert info['max_tokens'] == 1000
    
    @patch('src.llm_provider.requests.get')
    def test_invoke_with_retry(self, mock_get):
        """재시도 로직 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with patch('src.llm_provider.LLMProviderManager._initialize_llm'):
            provider = LLMProviderManager(
                provider='ollama',
                model='test-model',
                base_url='http://localhost:11434'
            )
            
            # Mock LLM 설정
            mock_llm = Mock()
            mock_llm.invoke.side_effect = [
                Exception("First attempt failed"),
                "Success on second attempt"
            ]
            provider.llm = mock_llm
            
            # 재시도 후 성공
            result = provider.invoke("test prompt", retry_count=3)
            assert result == "Success on second attempt"
            assert mock_llm.invoke.call_count == 2
    
    @patch('src.llm_provider.requests.get')
    def test_invoke_all_retries_failed(self, mock_get):
        """모든 재시도 실패 테스트"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with patch('src.llm_provider.LLMProviderManager._initialize_llm'):
            provider = LLMProviderManager(
                provider='ollama',
                model='test-model',
                base_url='http://localhost:11434'
            )
            
            # Mock LLM 설정 (모든 시도 실패)
            mock_llm = Mock()
            mock_llm.invoke.side_effect = Exception("Always fails")
            provider.llm = mock_llm
            
            # 모든 재시도 실패 시 예외 발생
            with pytest.raises(LLMConnectionError):
                provider.invoke("test prompt", retry_count=2)
