"""
빠른 테스트 스크립트
"""
import sys
sys.path.insert(0, '..')

from src.config_manager import ConfigManager
from src.llm_provider import LLMProviderManager
from src.display import DisplayManager

print("=" * 60)
print("Ollama 연결 테스트")
print("=" * 60)

# 설정 로드
config_manager = ConfigManager('../config/ollama_config.yaml')
llm_config = config_manager.get_llm_config()

print(f"\n설정:")
print(f"  Provider: {llm_config.provider}")
print(f"  Model: {llm_config.model}")
print(f"  Base URL: {llm_config.base_url}")

# Display 초기화
display = DisplayManager(show_timestamps=True, color_output=True)

try:
    print("\n연결 중...")
    llm_provider = LLMProviderManager(
        provider=llm_config.provider,
        model=llm_config.model,
        base_url=llm_config.base_url,
        temperature=llm_config.temperature,
        max_tokens=llm_config.max_tokens
    )
    
    print("✅ 연결 성공!")
    
    # 간단한 테스트
    print("\n간단한 질의 테스트...")
    test_prompt = "Hello, how are you? Please respond in one sentence."
    
    print(f"질의: {test_prompt}")
    print("응답 대기 중...")
    
    response = llm_provider.invoke(test_prompt)
    
    print(f"\n응답: {response}")
    print("\n✅ 테스트 완료!")
    
except Exception as e:
    print(f"\n❌ 오류: {e}")
    import traceback
    traceback.print_exc()
