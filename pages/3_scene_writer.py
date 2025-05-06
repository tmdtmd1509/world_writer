import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="회차 작성 및 중요도 태깅", layout="wide")
st.title("✍️ 회차 작성 및 중요도 태깅")

# 에피소드 선택
st.subheader("📘 에피소드 정보")
episode_title = st.text_input("소속 에피소드", placeholder="예: 붉은 달의 밤")
chapter_title = st.text_input("회차 제목", placeholder="예: 5-1. 붉은 달이 떠오르다")
chapter_outline = st.text_area("회차 개요", height=100)

# 회차 본문 입력
st.subheader("📝 회차 본문 작성")
raw_text = st.text_area("전체 회차 텍스트를 입력하세요 (자동 문장 분리됨)", height=300)

# 문장 분리 (간단한 줄바꿈 또는 마침표 기준)
lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
if not lines:
    st.warning("먼저 본문을 입력해 주세요.")
    st.stop()

# 중요도 태깅 UI
st.subheader("🎯 문장별 중요도 태깅")
tagged_lines = []

for i, line in enumerate(lines):
    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(f"**{i+1}.** {line}")
    with col2:
        importance = st.slider(f"중요도 (0.0~1.0)", 0.0, 1.0, 0.5, step=0.1, key=f"imp_{i}")
        tag = st.text_input(f"태그 (선택)", key=f"tag_{i}")
    tagged_lines.append({
        "line": line,
        "weight": importance,
        "tag": tag
    })

# 저장
st.markdown("---")
if st.button("💾 회차 저장"):
    chapter_data = {
        "episode_title": episode_title,
        "chapter_title": chapter_title,
        "outline": chapter_outline,
        "lines": tagged_lines,
        "created_at": datetime.now().isoformat()
    }

    os.makedirs("chapters", exist_ok=True)
    filename = f"chapters/{chapter_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chapter_data, f, ensure_ascii=False, indent=2)

    st.success(f"✅ 회차 저장 완료 → `{filename}`")
