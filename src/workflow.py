"""
LangGraph 워크플로우 모듈
"""
from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime
import time
from langgraph.graph import StateGraph, END


class WorkflowState(TypedDict):
    """워크플로우 상태"""
    original_query: str
    analysis: Optional[Dict[str, str]]
    optimized_prompt: Optional[str]
    llm_response: Optional[str]
    steps: List[Dict[str, Any]]
    timestamps: Dict[str, str]
    error: Optional[str]


class PromptOptimizationWorkflow:
    """프롬프트 최적화 워크플로우"""
    
    def __init__(self, llm_provider, prompt_optimizer, display_manager):
        """
        Args:
            llm_provider: LLMProviderManager 인스턴스
            prompt_optimizer: PromptOptimizer 인스턴스
            display_manager: DisplayManager 인스턴스
        """
        self.llm_provider = llm_provider
        self.prompt_optimizer = prompt_optimizer
        self.display = display_manager
        self.workflow = self._build_workflow()
        self.state_history: List[WorkflowState] = []
    
    def _build_workflow(self) -> StateGraph:
        """워크플로우 그래프 구성"""
        # StateGraph 생성
        workflow = StateGraph(WorkflowState)
        
        # 노드 추가
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("optimize", self._optimize_node)
        workflow.add_node("invoke_llm", self._invoke_llm_node)
        
        # 엣지 추가
        workflow.add_edge("analyze", "optimize")
        workflow.add_edge("optimize", "invoke_llm")
        workflow.add_edge("invoke_llm", END)
        
        # 시작점 설정
        workflow.set_entry_point("analyze")
        
        return workflow.compile()
    
    def _analyze_node(self, state: WorkflowState) -> WorkflowState:
        """
        질의 분석 노드
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        try:
            self.display.show_step(
                "1단계: 질의 분석",
                "사용자 질의의 명확성과 완전성을 분석합니다..."
            )
            
            # 질의 분석
            analysis = self.prompt_optimizer.analyze_query(state['original_query'])
            
            # 분석 결과 표시
            self.display.show_analysis_result(analysis)
            
            # 상태 업데이트
            state['analysis'] = analysis
            state['timestamps']['analyze'] = datetime.now().isoformat()
            state['steps'].append({
                'name': 'analyze',
                'timestamp': datetime.now().isoformat(),
                'status': 'completed'
            })
            
            # 상태 히스토리 저장
            self.state_history.append(state.copy())
            
        except Exception as e:
            state['error'] = f"분석 오류: {str(e)}"
            self.display.show_error(e, "질의 분석")
        
        return state
    
    def _optimize_node(self, state: WorkflowState) -> WorkflowState:
        """
        프롬프트 최적화 노드
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        try:
            # 이전 단계에서 오류가 있으면 스킵
            if state.get('error'):
                return state
            
            self.display.show_step(
                "2단계: 프롬프트 최적화",
                "분석 결과를 바탕으로 프롬프트를 개선합니다..."
            )
            
            # 프롬프트 최적화
            optimized = self.prompt_optimizer.optimize_prompt(
                state['original_query'],
                state['analysis']
            )
            
            # 의도 보존 검증
            intent_preserved = self.prompt_optimizer.check_intent_preservation(
                state['original_query'],
                optimized
            )
            
            if not intent_preserved:
                self.display.show_warning(
                    "원본 질의의 의도가 일부 변경되었을 수 있습니다."
                )
            
            # 최적화된 프롬프트 표시
            self.display.show_optimized_prompt(optimized)
            
            # 상태 업데이트
            state['optimized_prompt'] = optimized
            state['timestamps']['optimize'] = datetime.now().isoformat()
            state['steps'].append({
                'name': 'optimize',
                'timestamp': datetime.now().isoformat(),
                'status': 'completed',
                'intent_preserved': intent_preserved
            })
            
            # 상태 히스토리 저장
            self.state_history.append(state.copy())
            
        except Exception as e:
            state['error'] = f"최적화 오류: {str(e)}"
            self.display.show_error(e, "프롬프트 최적화")
        
        return state
    
    def _invoke_llm_node(self, state: WorkflowState) -> WorkflowState:
        """
        LLM 호출 노드
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        try:
            # 이전 단계에서 오류가 있으면 스킵
            if state.get('error'):
                return state
            
            self.display.show_step(
                "3단계: LLM 호출",
                "최적화된 프롬프트로 LLM에 질의합니다..."
            )
            
            # LLM 호출 시간 측정
            start_time = time.time()
            response = self.llm_provider.invoke(state['optimized_prompt'])
            duration = time.time() - start_time
            
            # 응답 표시
            self.display.show_llm_response(response, duration)
            
            # 상태 업데이트
            state['llm_response'] = response
            state['timestamps']['invoke_llm'] = datetime.now().isoformat()
            state['steps'].append({
                'name': 'invoke_llm',
                'timestamp': datetime.now().isoformat(),
                'status': 'completed',
                'duration': duration
            })
            
            # 상태 히스토리 저장
            self.state_history.append(state.copy())
            
        except Exception as e:
            state['error'] = f"LLM 호출 오류: {str(e)}"
            self.display.show_error(e, "LLM 호출")
        
        return state
    
    def run(self, query: str) -> WorkflowState:
        """
        워크플로우 실행
        
        Args:
            query: 사용자 질의
            
        Returns:
            최종 상태
        """
        # 초기 상태 생성
        initial_state: WorkflowState = {
            'original_query': query,
            'analysis': None,
            'optimized_prompt': None,
            'llm_response': None,
            'steps': [],
            'timestamps': {'start': datetime.now().isoformat()},
            'error': None
        }
        
        # 원본 질의 표시
        self.display.show_original_query(query)
        
        # 워크플로우 실행
        final_state = self.workflow.invoke(initial_state)
        
        # 종료 타임스탬프 추가
        final_state['timestamps']['end'] = datetime.now().isoformat()
        
        return final_state
    
    def get_state_history(self) -> List[WorkflowState]:
        """
        상태 히스토리 반환
        
        Returns:
            상태 히스토리 리스트
        """
        return self.state_history
    
    def clear_history(self):
        """상태 히스토리 초기화"""
        self.state_history = []
