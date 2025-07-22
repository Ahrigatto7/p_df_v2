import os
from typing import List
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_tags(text: str, max_tags: int = 5) -> List[str]:
    if not openai.api_key:
        return []
    prompt = f"다음 문서 내용에서 핵심 키워드 {max_tags}개를 한국어로 추출해 주세요.\n{text[:1000]}"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = resp.choices[0].message.content
        tags = [t.strip() for t in content.split(',')]
        return tags[:max_tags]
    except Exception:
        return []
