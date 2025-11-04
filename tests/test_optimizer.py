"""
PromptOptimizer 테스트
"""
import pytest
from unittest.mock import Mock, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.prompt_optimizer import PromptOptimizer, OptimizationError, OptimizationStep


class TestPromptOptimizer:
    """PromptOptimizer 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.mock_llm_provider = Mock()
        self.optimizer = PromptOptimizer(self.mock_llm_provider)
    
    def test_analyze_query_success(self):
        """질의 분석 성공 테스트"""
        # Mock LLM 응답
        self.mock_llm_provider.invoke.return_value = """
        명확성: 7/10 - 기본적인 의도는 명확
        완전성: 6/10 - 일부 정보 부족
        컨텍스트: 추가 정보 필요
        """
        
        query = "파이썬으로 웹 스크래핑하는 방법"
        analysis = self.optimizer.analyze_query(query)
        
        assert isinstance(analysis, dict)
        assert '명확성' in analysis
        assert '완전성' in analysis
        assert '컨텍스트' in analysis
        
        # 최적화 단계가 기록되었는지 확인
        steps = self.optimizer.get_optimization_steps()
        assert len(steps) == 1
        assert steps[0].name == "질의 분석"
    
    def test_analyze_query_empty(self):
        """빈 질의 분석 테스트"""
        with pytest.raises(OptimizationError, match="빈 질의"):
            self.optimizer.analyze_query("")
    
    def test_analyze_query_too_long(self):
        """너무 긴 질의 분석 테스트"""
        long_query = "a" * 6000
        
        with pytest.raises(OptimizationError, match="너무 깁니다"):
            self.optimizer.analyze_query(long_query)
    
    def test_optimize_prompt_success(self):
        """프롬프트 최적화 성공 테스트"""
        # Mock LLM 응답
        self.mock_llm_provider.invoke.return_value = """
        Python을 사용하여 웹 스크래핑을 수행하는 방법을 단계별로 설명해주세요.
        BeautifulSoup과 requests 라이브러리를 사용한 예제를 포함해주세요.
        """
        
        query = "파이썬으로 웹 스크래핑"
        analysis = {
            '명확성': '7/10',
            '완전성': '6/10',
            '컨텍스트': '라이브러리 정보 필요'
        }
        
        optimized = self.optimizer.optimize_prompt(query, analysis)
        
        assert isinstance(optimized, str)
        assert len(optimized) > 0
        
        # 최적화 단계가 기록되었는지 확인
        steps = self.optimizer.get_optimization_steps()
        assert len(steps) == 1
        assert steps[0].name == "프롬프트 최적화"
    
    def test_check_intent_preservation_preserved(self):
        """의도 보존 검증 - 보존됨"""
        original = "파이썬으로 웹 스크래핑하는 방법"
        optimized = "Python을 사용하여 웹 스크래핑을 수행하는 방법을 설명해주세요"
        
        preserved = self.optimizer.check_intent_preservation(original, optimized)
        assert preserved == True
    
    def test_check_intent_preservation_not_preserved(self):
        """의도 보존 검증 - 보존 안됨"""
        original = "파이썬으로 웹 스크래핑하는 방법"
        optimized = "자바스크립트로 데이터베이스 설계하는 방법"
        
        preserved = self.optimizer.check_intent_preservation(original, optimized)
        assert preserved == False
    
    def test_is_well_formed_true(self):
        """잘 구성된 질의 확인 - True"""
        query = "파이썬으로 웹 스크래핑을 하는 방법을 알려주세요."
        
        assert self.optimizer.is_well_formed(query) == True
    
    def test_is_well_formed_too_short(self):
        """잘 구성된 질의 확인 - 너무 짧음"""
        query = "파이썬"
        
        assert self.optimizer.is_well_formed(query) == False
    
    def test_is_well_formed_no_punctuation(self):
        """잘 구성된 질의 확인 - 마침표 없음"""
        query = "파이썬으로 웹 스크래핑하는 방법"
        
        assert self.optimizer.is_well_formed(query) == False
    
    def test_is_well_formed_too_few_words(self):
        """잘 구성된 질의 확인 - 단어 수 부족"""
        query = "파이썬 웹."
        
        assert self.optimizer.is_well_formed(query) == False
    
    def test_get_optimization_steps(self):
        """최적화 단계 목록 반환 테스트"""
        # Mock LLM 응답
        self.mock_llm_provider.invoke.return_value = "분석 결과"
        
        query = "테스트 질의입니다."
        self.optimizer.analyze_query(query)
        
        steps = self.optimizer.get_optimization_steps()
        
        assert isinstance(steps, list)
        assert len(steps) == 1
        assert isinstance(steps[0], OptimizationStep)
    
    def test_clear_steps(self):
        """최적화 단계 초기화 테스트"""
        # Mock LLM 응답
        self.mock_llm_provider.invoke.return_value = "분석 결과"
        
        query = "테스트 질의입니다."
        self.optimizer.analyze_query(query)
        
        assert len(self.optimizer.get_optimization_steps()) == 1
        
        self.optimizer.clear_steps()
        
        assert len(self.optimizer.get_optimization_steps()) == 0
    
    def test_analyze_query_llm_error(self):
        """LLM 오류 시 분석 실패 테스트"""
        # Mock LLM이 예외 발생
        self.mock_llm_provider.invoke.side_effect = Exception("LLM error")
        
        query = "테스트 질의입니다."
        
        with pytest.raises(OptimizationError, match="질의 분석 실패"):
            self.optimizer.analyze_query(query)
    
    def test_optimize_prompt_llm_error(self):
        """LLM 오류 시 최적화 실패 테스트"""
        # Mock LLM이 예외 발생
        self.mock_llm_provider.invoke.side_effect = Exception("LLM error")
        
        query = "테스트 질의입니다."
        analysis = {'명확성': '7/10'}
        
        with pytest.raises(OptimizationError, match="프롬프트 최적화 실패"):
            self.optimizer.optimize_prompt(query, analysis)
