import streamlit as st
import os
import json
from utils.summarizer import summarize_chapter

st.set_page_config(page_title="🧠 회차 요약 자동화", layout="wide")
st.title("🧠 회차 요약 자동 생성기")

st.markdown("작성한 회차 중 하나를 선택해 GPT를 통해 요약을 생성하고 저장할 수 있습니다.")

# 📂 회차 파일 목록 가져오기
chapter_files = [
    f for f in os.listdir("chapters") if f.endswith(".json")
]

if not chapter_files:
    st.warning("회차 파일이 없습니다. 먼저 회차를 작성하고 저장해 주세요.")
    st.stop()

# 🧾 회차 선택
selected_file = st.selectbox("요약할 회차 선택", chapter_files)

# 🔍 회차 내용 미리 보기
with open(os.path.join("chapters", selected_file), "r", encoding="utf-8") as f:
    chapter_data = json.load(f)

st.subheader("✍️ 회차 개요")
st.write(f"제목: {chapter_data.get('chapter_title')}")
st.write(f"개요: {chapter_data.get('outline')}")

st.subheader("🔎 일부 본문 미리 보기")
for line in chapter_data["lines"][:5]:
    st.markdown(f"- {line['line']}")

# 🧠 요약 버튼
if st.button("🤖 GPT로 요약 생성 및 저장"):
    try:
        summary = summarize_chapter(os.path.join("chapters", selected_file))
        st.success("✅ 요약이 성공적으로 생성되어 저장되었습니다.")
        st.markdown("### ✨ 생성된 요약:")
        st.markdown(summary)
    except Exception as e:
        st.error(f"요약 중 오류 발생: {str(e)}")
