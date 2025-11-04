"""
프롬프트 최적화 모듈
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OptimizationStep:
    """최적화 단계"""
    name: str
    description: str
    timestamp: datetime
    input_data: str
    output_data: str


class OptimizationError(Exception):
    """최적화 오류"""
    pass


class PromptOptimizer:
    """프롬프트 분석 및 최적화"""
    
    def __init__(self, llm_provider):
        """
        Args:
            llm_provider: LLMProviderManager 인스턴스
        """
        self.llm_provider = llm_provider
        self.optimization_steps: List[OptimizationStep] = []
    
    def analyze_query(self, query: str) -> Dict[str, str]:
        """
        질의 분석
        
        Args:
            query: 사용자 질의
            
        Returns:
            분석 결과 딕셔너리
        """
        if not query or not query.strip():
            raise OptimizationError("빈 질의는 분석할 수 없습니다.")
        
        # 질의 길이 확인
        query_length = len(query)
        if query_length > 5000:
            raise OptimizationError("질의가 너무 깁니다 (최대 5000자).")
        
        # LLM을 사용한 질의 분석 (단순화된 프롬프트)
        analysis_prompt = f"""Analyze this query and rate it:

Query: {query}

Rate these aspects (1-10):
1. Clarity: How clear is the query?
2. Completeness: Is enough information provided?
3. Context: What context would help?

Answer briefly in 3 lines."""

        try:
            analysis_response = self.llm_provider.invoke(analysis_prompt)
            
            # 분석 결과 파싱 (간단한 파싱)
            analysis = {
                '명확성': '분석 중',
                '완전성': '분석 중',
                '컨텍스트': '분석 중'
            }
            
            # 응답에서 정보 추출 시도
            lines = analysis_response.strip().split('\n')
            for line in lines:
                if '명확성' in line:
                    analysis['명확성'] = line.split(':', 1)[-1].strip() if ':' in line else line
                elif '완전성' in line:
                    analysis['완전성'] = line.split(':', 1)[-1].strip() if ':' in line else line
                elif '컨텍스트' in line:
                    analysis['컨텍스트'] = line.split(':', 1)[-1].strip() if ':' in line else line
            
            # 단계 기록
            self.optimization_steps.append(OptimizationStep(
                name="질의 분석",
                description="사용자 질의의 명확성과 완전성 평가",
                timestamp=datetime.now(),
                input_data=query,
                output_data=str(analysis)
            ))
            
            return analysis
            
        except Exception as e:
            raise OptimizationError(f"질의 분석 실패: {e}")
    
    def optimize_prompt(self, query: str, analysis: Dict[str, str]) -> str:
        """
        프롬프트 최적화
        
        Args:
            query: 원본 질의
            analysis: 분석 결과
            
        Returns:
            최적화된 프롬프트
        """
        # 최적화 프롬프트 생성 (단순화)
        optimization_prompt = f"""Improve this query to be more clear and effective.

Original query: {query}

Analysis: {self._format_analysis(analysis)}

Guidelines:
1. Keep the core intent
2. Be more specific
3. Add helpful context
4. Use structured format

Output only the improved prompt without explanation."""

        try:
            optimized = self.llm_provider.invoke(optimization_prompt)
            
            # 최적화 결과 정리
            optimized = optimized.strip()
            
            # 단계 기록
            self.optimization_steps.append(OptimizationStep(
                name="프롬프트 최적화",
                description="분석 결과를 바탕으로 프롬프트 개선",
                timestamp=datetime.now(),
                input_data=query,
                output_data=optimized
            ))
            
            return optimized
            
        except Exception as e:
            raise OptimizationError(f"프롬프트 최적화 실패: {e}")
    
    def _format_analysis(self, analysis: Dict[str, str]) -> str:
        """분석 결과 포맷팅"""
        formatted = []
        for key, value in analysis.items():
            formatted.append(f"- {key}: {value}")
        return '\n'.join(formatted)
    
    def check_intent_preservation(self, original: str, optimized: str) -> bool:
        """
        의도 보존 검증
        
        Args:
            original: 원본 질의
            optimized: 최적화된 프롬프트
            
        Returns:
            의도가 보존되었는지 여부
        """
        # 간단한 검증: 주요 키워드가 유지되는지 확인
        # 실제로는 더 정교한 검증이 필요할 수 있음
        
        # 원본의 주요 단어 추출 (간단한 방법)
        original_words = set(original.lower().split())
        optimized_words = set(optimized.lower().split())
        
        # 공통 단어 비율 계산
        if len(original_words) == 0:
            return False
        
        common_words = original_words.intersection(optimized_words)
        preservation_ratio = len(common_words) / len(original_words)
        
        # 50% 이상의 단어가 유지되면 의도가 보존된 것으로 간주
        return preservation_ratio >= 0.3
    
    def is_well_formed(self, query: str) -> bool:
        """
        질의가 잘 구성되었는지 확인
        
        Args:
            query: 질의
            
        Returns:
            잘 구성되었는지 여부
        """
        # 간단한 휴리스틱
        # 1. 적절한 길이 (20자 이상)
        if len(query) < 20:
            return False
        
        # 2. 완전한 문장 (마침표, 물음표 등으로 끝남)
        if not query.strip()[-1] in '.?!':
            return False
        
        # 3. 여러 단어로 구성
        if len(query.split()) < 5:
            return False
        
        return True
    
    def get_optimization_steps(self) -> List[OptimizationStep]:
        """
        최적화 단계 목록 반환
        
        Returns:
            최적화 단계 리스트
        """
        return self.optimization_steps
    
    def clear_steps(self):
        """최적화 단계 초기화"""
        self.optimization_steps = []
