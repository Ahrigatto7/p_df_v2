import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def prepare_data():
    """Return concept texts and case dictionaries."""
    concepts = [
        "대운/세운의 응기 정의 및 메커니즘",
        "출현/인동/합충형파에 따른 응기 작용",
        "대운과 세운의 차이와 응기의 실제 적용 방식",
        "허실 판단 방법",
        "십신(정관, 편관, 식신, 상관, 비견, 겁재 등)의 성격",
        "천간/지지/궁위의 의미와 역할",
        "제압 방식, 구조, 格(격)의 성립 조건",
        "기타 실전 해석 기법",
    ]

    cases = [
        {"id": 1, "title": "전기 감전사고로 사망", "content": "대운·세운의 간합과 제압으로 인해 사망한 응기 분석"},
        {"id": 2, "title": "적포구조", "content": "관살 제압 실패로 인한 재정 문제 분석"},
        {"id": 3, "title": "군인 사망", "content": "자합 및 반국 구조로 사망 발생 이유"},
    ]
    return concepts, cases


def extract_keywords(texts, top_k=5):
    """Simple TF-IDF based keyword extractor."""
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)
    features = vectorizer.get_feature_names_out()
    keywords = []
    for row in X.toarray():
        top_indices = row.argsort()[-top_k:][::-1]
        keywords.append([features[i] for i in top_indices])
    return keywords


def save_concepts_excel(concepts, keywords, path="concepts.xlsx"):
    df = pd.DataFrame({"concept": concepts, "keywords": [", ".join(k) for k in keywords]})
    df.to_excel(path, index=False)


def save_cases_excel(cases, keywords, path="cases_summary.xlsx"):
    summaries = [c["content"][:50] + "..." for c in cases]
    df = pd.DataFrame({
        "id": [c["id"] for c in cases],
        "title": [c["title"] for c in cases],
        "summary": summaries,
        "keywords": [", ".join(k) for k in keywords],
    })
    df.to_excel(path, index=False)


def main():
    concepts, cases = prepare_data()
    concept_kw = extract_keywords(concepts)
    case_kw = extract_keywords([c["content"] for c in cases])

    save_concepts_excel(concepts, concept_kw)
    save_cases_excel(cases, case_kw)

    # Save individual case files
    os.makedirs("cases", exist_ok=True)
    for c in cases:
        with open(os.path.join("cases", f"case_{c['id']}.txt"), "w", encoding="utf-8") as f:
            f.write(c["content"])


if __name__ == "__main__":
    main()
