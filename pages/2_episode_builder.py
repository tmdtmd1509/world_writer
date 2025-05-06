import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="에피소드 설정 입력기", layout="wide")
st.title("📖 에피소드 설정 입력기 (Episode Builder)")

# --- 기본 입력
st.subheader("📝 에피소드 정보")

episode_title = st.text_input("에피소드 제목", placeholder="예: 붉은 달의 밤")
episode_description = st.text_area("에피소드 설명", height=100)
start_status = st.text_area("에피소드 시작 상태", placeholder="예: 루벤은 여전히 복수심에 불타며 갈등 상태에 있음")
end_goal = st.text_area("에피소드의 최종 목표", placeholder="예: 루벤은 진실을 알게 되어 혼란에 빠짐")

# --- 필수 포함 요소
st.subheader("📌 반드시 포함할 사건")

must_include_raw = st.text_area("한 줄에 하나씩 입력", height=100)
must_include = [line.strip() for line in must_include_raw.split("\n") if line.strip()]

# --- 등장 인물
st.subheader("👤 중심 등장 인물")
characters_involved_raw = st.text_input("쉼표로 구분된 인물 이름", placeholder="루벤, 엘렌")
characters_involved = [c.strip() for c in characters_involved_raw.split(",") if c.strip()]

# --- 주제/분위기
st.subheader("🎭 분위기 및 주제")
theme = st.text_input("예: 긴장감, 배신, 진실에의 접근")

# --- 설정 참조 ID
st.subheader("🧠 연결할 설정 요소 ID")
ref_settings = st.text_input("쉼표로 구분된 ID (예: characters.루벤, magic_systems.에테르 마법)")
reference_setting_ids = [s.strip() for s in ref_settings.split(",") if s.strip()]

# --- 저장
if st.button("💾 에피소드 저장"):
    episode_data = {
        "title": episode_title,
        "description": episode_description,
        "start_status": start_status,
        "end_goal": end_goal,
        "must_include": must_include,
        "characters_involved": characters_involved,
        "theme": theme,
        "reference_setting_ids": reference_setting_ids
    }

    os.makedirs("episodes", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"episodes/{episode_title or 'episode'}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(episode_data, f, ensure_ascii=False, indent=2)

    st.success(f"✅ 에피소드 저장 완료! → `{filename}`")
