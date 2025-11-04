"""
PromptOptimizationWorkflow 통합 테스트
"""
import pytest
from unittest.mock import Mock, MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.workflow import PromptOptimizationWorkflow, WorkflowState
from src.llm_provider import LLMProviderManager
from src.prompt_optimizer import PromptOptimizer
from src.display import DisplayManager


class TestPromptOptimizationWorkflow:
    """PromptOptimizationWorkflow 통합 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        # Mock 컴포넌트 생성
        self.mock_llm_provider = Mock(spec=LLMProviderManager)
        self.mock_prompt_optimizer = Mock(spec=PromptOptimizer)
        self.mock_display = Mock(spec=DisplayManager)
        
        # Workflow 초기화
        self.workflow = PromptOptimizationWorkflow(
            self.mock_llm_provider,
            self.mock_prompt_optimizer,
            self.mock_display
        )
    
    def test_workflow_initialization(self):
        """워크플로우 초기화 테스트"""
        assert self.workflow.llm_provider is not None
        assert self.workflow.prompt_optimizer is not None
        assert self.workflow.display is not None
        assert self.workflow.workflow is not None
    
    def test_analyze_node_success(self):
        """분석 노드 성공 테스트"""
        # Mock 분석 결과
        mock_analysis = {
            '명확성': '7/10',
            '완전성': '6/10',
            '컨텍스트': '추가 정보 필요'
        }
        self.mock_prompt_optimizer.analyze_query.return_value = mock_analysis
        
        # 초기 상태
        state: WorkflowState = {
            'original_query': '테스트 질의',
            'analysis': None,
            'optimized_prompt': None,
            'llm_response': None,
            'steps': [],
            'timestamps': {},
            'error': None
        }
        
        # 분석 노드 실행
        result_state = self.workflow._analyze_node(state)
        
        # 검증
        assert result_state['analysis'] == mock_analysis
        assert 'analyze' in result_state['timestamps']
        assert len(result_state['steps']) == 1
        assert result_state['steps'][0]['name'] == 'analyze'
        assert result_state['error'] is None
    
    def test_analyze_node_error(self):
        """분석 노드 오류 테스트"""
        # Mock이 예외 발생
        self.mock_prompt_optimizer.analyze_query.side_effect = Exception("분석 오류")
        
        state: WorkflowState = {
            'original_query': '테스트 질의',
            'analysis': None,
            'optimized_prompt': None,
            'llm_response': None,
            'steps': [],
            'timestamps': {},
            'error': None
        }
        
        result_state = self.workflow._analyze_node(state)
        
        # 오류가 기록되어야 함
        assert result_state['error'] is not None
        assert '분석 오류' in result_state['error']
    
    def test_optimize_node_success(self):
        """최적화 노드 성공 테스트"""
        # Mock 최적화 결과
        mock_optimized = "최적화된 프롬프트입니다."
        self.mock_prompt_optimizer.optimize_prompt.return_value = mock_optimized
        self.mock_prompt_optimizer.check_intent_preservation.return_value = True
        
        state: WorkflowState = {
            'original_query': '테스트 질의',
            'analysis': {'명확성': '7/10'},
            'optimized_prompt': None,
            'llm_response': None,
            'steps': [],
            'timestamps': {},
            'error': None
        }
        
        result_state = self.workflow._optimize_node(state)
        
        assert result_state['optimized_prompt'] == mock_optimized
        assert 'optimize' in result_state['timestamps']
        assert len(result_state['steps']) == 1
        assert result_state['error'] is None
    
    def test_optimize_node_skip_on_error(self):
        """이전 오류 시 최적화 노드 스킵 테스트"""
        state: WorkflowState = {
            'original_query': '테스트 질의',
            'analysis': None,
            'optimized_prompt': None,
            'llm_response': None,
            'steps': [],
            'timestamps': {},
            'error': '이전 단계 오류'
        }
        
        result_state = self.workflow._optimize_node(state)
        
        # 최적화가 실행되지 않아야 함
        assert result_state['optimized_prompt'] is None
        assert result_state['error'] == '이전 단계 오류'
    
    def test_invoke_llm_node_success(self):
        """LLM 호출 노드 성공 테스트"""
        # Mock LLM 응답
        mock_response = "LLM의 응답입니다."
        self.mock_llm_provider.invoke.return_value = mock_response
        
        state: WorkflowState = {
            'original_query': '테스트 질의',
            'analysis': {'명확성': '7/10'},
            'optimized_prompt': '최적화된 프롬프트',
            'llm_response': None,
            'steps': [],
            'timestamps': {},
            'error': None
        }
        
        result_state = self.workflow._invoke_llm_node(state)
        
        assert result_state['llm_response'] == mock_response
        assert 'invoke_llm' in result_state['timestamps']
        assert len(result_state['steps']) == 1
        assert 'duration' in result_state['steps'][0]
        assert result_state['error'] is None
    
    def test_invoke_llm_node_skip_on_error(self):
        """이전 오류 시 LLM 호출 노드 스킵 테스트"""
        state: WorkflowState = {
            'original_query': '테스트 질의',
            'analysis': None,
            'optimized_prompt': None,
            'llm_response': None,
            'steps': [],
            'timestamps': {},
            'error': '이전 단계 오류'
        }
        
        result_state = self.workflow._invoke_llm_node(state)
        
        # LLM 호출이 실행되지 않아야 함
        assert result_state['llm_response'] is None
        assert result_state['error'] == '이전 단계 오류'
    
    def test_run_workflow_success(self):
        """전체 워크플로우 실행 성공 테스트"""
        # Mock 설정
        self.mock_prompt_optimizer.analyze_query.return_value = {'명확성': '7/10'}
        self.mock_prompt_optimizer.optimize_prompt.return_value = '최적화된 프롬프트'
        self.mock_prompt_optimizer.check_intent_preservation.return_value = True
        self.mock_llm_provider.invoke.return_value = 'LLM 응답'
        
        # 워크플로우 실행
        query = '테스트 질의입니다.'
        final_state = self.workflow.run(query)
        
        # 검증
        assert final_state['original_query'] == query
        assert final_state['analysis'] is not None
        assert final_state['optimized_prompt'] is not None
        assert final_state['llm_response'] is not None
        assert 'start' in final_state['timestamps']
        assert 'end' in final_state['timestamps']
        assert final_state['error'] is None
    
    def test_get_state_history(self):
        """상태 히스토리 반환 테스트"""
        # Mock 설정
        self.mock_prompt_optimizer.analyze_query.return_value = {'명확성': '7/10'}
        self.mock_prompt_optimizer.optimize_prompt.return_value = '최적화된 프롬프트'
        self.mock_prompt_optimizer.check_intent_preservation.return_value = True
        self.mock_llm_provider.invoke.return_value = 'LLM 응답'
        
        # 워크플로우 실행
        self.workflow.run('테스트 질의')
        
        # 히스토리 확인
        history = self.workflow.get_state_history()
        
        assert isinstance(history, list)
        assert len(history) > 0
    
    def test_clear_history(self):
        """상태 히스토리 초기화 테스트"""
        # Mock 설정
        self.mock_prompt_optimizer.analyze_query.return_value = {'명확성': '7/10'}
        self.mock_prompt_optimizer.optimize_prompt.return_value = '최적화된 프롬프트'
        self.mock_prompt_optimizer.check_intent_preservation.return_value = True
        self.mock_llm_provider.invoke.return_value = 'LLM 응답'
        
        # 워크플로우 실행
        self.workflow.run('테스트 질의')
        
        assert len(self.workflow.get_state_history()) > 0
        
        # 히스토리 초기화
        self.workflow.clear_history()
        
        assert len(self.workflow.get_state_history()) == 0
    
    def test_workflow_with_intent_not_preserved(self):
        """의도 보존 안됨 경고 테스트"""
        # Mock 설정
        self.mock_prompt_optimizer.analyze_query.return_value = {'명확성': '7/10'}
        self.mock_prompt_optimizer.optimize_prompt.return_value = '최적화된 프롬프트'
        self.mock_prompt_optimizer.check_intent_preservation.return_value = False  # 의도 보존 안됨
        self.mock_llm_provider.invoke.return_value = 'LLM 응답'
        
        # 워크플로우 실행
        final_state = self.workflow.run('테스트 질의')
        
        # 경고가 표시되었는지 확인
        self.mock_display.show_warning.assert_called()
        
        # 워크플로우는 계속 진행되어야 함
        assert final_state['llm_response'] is not None


class TestWorkflowIntegration:
    """실제 컴포넌트를 사용한 통합 테스트 (Mock LLM 사용)"""
    
    @patch('src.llm_provider.requests.get')
    def test_full_workflow_with_mocked_llm(self, mock_get):
        """Mock LLM을 사용한 전체 워크플로우 테스트"""
        # 연결 검증 Mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # LLM Provider Mock
        with patch('src.llm_provider.LLMProviderManager._initialize_llm'):
            mock_llm_provider = Mock(spec=LLMProviderManager)
            mock_llm_provider.invoke.return_value = "Mock LLM 응답"
            
            # 실제 컴포넌트 생성
            prompt_optimizer = PromptOptimizer(mock_llm_provider)
            display = DisplayManager(show_timestamps=False, color_output=False)
            workflow = PromptOptimizationWorkflow(
                mock_llm_provider,
                prompt_optimizer,
                display
            )
            
            # 워크플로우 실행
            query = "테스트 질의입니다."
            final_state = workflow.run(query)
            
            # 검증
            assert final_state['original_query'] == query
            assert final_state['error'] is None or 'LLM' not in final_state['error']
