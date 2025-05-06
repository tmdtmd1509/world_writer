import openai
import json
import os
import streamlit as st  # secrets 사용을 위해 필요

# ✅ API 키를 secrets.toml 에서 불러오기
openai.api_key = st.secrets["openai"]["api_key"]

def summarize_chapter(chapter_path):
    with open(chapter_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    important_lines = "\n".join(
        [f"{i+1}. \"{line['line']}\" ({line['tag'] or '태그 없음'}, 중요도 {line['weight']})"
         for i, line in enumerate(data["lines"]) if line["weight"] >= 0.6]
    )
    full_text = "\n".join([line["line"] for line in data["lines"]])

    prompt = f"""
다음은 소설 회차의 정보입니다.

회차 개요: {data.get('outline', '없음')}
중요 문장:
{important_lines}

전체 회차 본문:
\"\"\"
{full_text}
\"\"\"

이 내용을 바탕으로 3~5문장으로 요약해 주세요.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 전문적인 소설 요약 AI입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    summary = response["choices"][0]["message"]["content"].strip()
    data["summary"] = summary

    with open(chapter_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return summary
