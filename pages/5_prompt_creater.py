import streamlit as st
import json
import os

st.set_page_config(page_title="🤖 프롬프트 자동 생성기", layout="wide")
st.title("🤖 다음 회차용 프롬프트 자동 생성기")

# --- 파일 선택
def get_file_list(folder):
    return [f for f in os.listdir(folder) if f.endswith(".json")]

world_file = st.selectbox("🌍 세계관 선택", get_file_list("worlds"))
episode_file = st.selectbox("📘 에피소드 선택", get_file_list("episodes"))
chapter_files = st.multiselect("📖 앞 회차 선택 (요약 포함)", get_file_list("chapters"))

# --- 불러오기
def load_json(folder, filename):
    with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
        return json.load(f)

if world_file and episode_file and chapter_files:
    world = load_json("worlds", world_file)
    episode = load_json("episodes", episode_file)
    chapters = [load_json("chapters", f) for f in chapter_files]

    # --- 요약과 중요 문장 합치기
    chapter_summaries = "\n".join([f"- {ch.get('summary', '요약 없음')}" for ch in chapters])
    important_lines = []
    for ch in chapters:
        for line in ch["lines"]:
            if line["weight"] >= 0.6:
                important_lines.append(f"- {line['line']} (중요도: {line['weight']}, 태그: {line['tag']})")
    important_text = "\n".join(important_lines)

    # --- 프롬프트 생성
    st.subheader("📄 생성된 프롬프트")

    prompt = f"""
당신은 소설 작가의 AI 보조자입니다.
다음 정보를 바탕으로 새로운 회차를 작성하는 데 도움이 되는 내용을 생성해 주세요.

🌍 세계관 요약:
- 제목: {world['title']}
- 설명: {world['description']}
- 마법 시스템: {[m['name'] for m in world.get('magic_systems', [])]}

📘 현재 에피소드:
- 제목: {episode['title']}
- 목표: {episode['end_goal']}
- 분위기: {episode['theme']}
- 반드시 포함할 사건: {episode['must_include']}

📖 앞 회차 요약:
{chapter_summaries}

🎯 이전 회차에서 중요한 문장:
{important_text}

🧾 지금부터 새로운 회차를 작성하세요. 에피소드 목표와 플롯 흐름에 맞춰 자연스럽게 이어지는 장면을 구성해 주세요.
"""

    st.code(prompt, language="markdown")

    if st.button("📋 복사 완료"):
        st.success("프롬프트가 복사되었습니다!")
else:
    st.warning("파일을 모두 선택해 주세요.")
