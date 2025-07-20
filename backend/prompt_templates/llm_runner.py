import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def run_prompt_template(template_str: str, variables: dict, model: str = "gpt-4", max_tokens: int = 512, temperature: float = 0.0) -> str:
    """
    템플릿 문자열과 변수 맵을 받아 LLM 응답을 반환합니다.
    """
    try:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

        # LangChain PromptTemplate 사용
        prompt = PromptTemplate.from_template(template_str)

        # 모델 초기화
        llm = ChatOpenAI(
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=openai_key
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        # 템플릿 실행
        return chain.run(variables).strip()

    except KeyError as e:
        return f"❌ 누락된 변수: {e}"
    except Exception as e:
        return f"❌ 실행 중 오류 발생: {str(e)}"
