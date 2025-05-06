import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="세계관 설정 입력기", layout="wide")
st.title("🌍 세계관 설정 입력기 (Story World Builder)")

# --- Session state 초기화
if "characters" not in st.session_state:
    st.session_state.characters = []

if "locations" not in st.session_state:
    st.session_state.locations = []

if "magic_systems" not in st.session_state:
    st.session_state.magic_systems = []

# --- 세계관 기본 정보
st.subheader("📘 세계관 개요")

title = st.text_input("세계관 이름")
description = st.text_area("세계 설명", height=150)

# --- 캐릭터 입력
st.subheader("👤 캐릭터 정보 추가")

with st.form(key="add_character_form"):
    char_name = st.text_input("이름")
    char_role = st.text_input("역할")
    char_traits = st.text_input("성격 (쉼표로 구분)", placeholder="고집, 충동, 복수심")
    char_goal = st.text_input("목표")
    char_backstory = st.text_area("과거사", height=100)
    if st.form_submit_button("캐릭터 추가"):
        st.session_state.characters.append({
            "name": char_name,
            "role": char_role,
            "traits": [t.strip() for t in char_traits.split(",") if t.strip()],
            "goal": char_goal,
            "backstory": char_backstory
        })

# 캐릭터 미리보기
if st.session_state.characters:
    st.markdown("✅ 현재 추가된 캐릭터:")
    for c in st.session_state.characters:
        st.markdown(f"- **{c['name']}** ({c['role']}): {', '.join(c['traits'])}")

# --- 지역 입력
st.subheader("🗺️ 지역 정보 추가")

with st.form(key="add_location_form"):
    loc_name = st.text_input("지역 이름")
    loc_desc = st.text_area("지역 설명", height=80)
    loc_history = st.text_area("지역 역사,사건", height=70)
    if st.form_submit_button("지역 추가"):
        st.session_state.locations.append({
            "name": loc_name,
            "description": loc_desc,
            "history": loc_history
        })

# 지역 미리보기
if st.session_state.locations:
    st.markdown("✅ 현재 추가된 지역:")
    for l in st.session_state.locations:
        st.markdown(f"- **{l['name']}**: {l['description']}")

# --- 마법 시스템 입력
st.subheader("🌀시스템 추가")

with st.form(key="add_magic_form"):
    magic_name = st.text_input("마법 이름")
    magic_rules = st.text_area("마법 룰 (한 줄에 하나씩 입력)", height=100)
    if st.form_submit_button("마법 시스템 추가"):
        rules = [r.strip() for r in magic_rules.split("\n") if r.strip()]
        st.session_state.magic_systems.append({
            "name": magic_name,
            "rules": rules
        })

# 마법 시스템 미리보기
if st.session_state.magic_systems:
    st.markdown("✅ 현재 추가된 마법 시스템:")
    for m in st.session_state.magic_systems:
        st.markdown(f"- **{m['name']}**: {', '.join(m['rules'])}")

# --- 세계관 룰
st.subheader("📜 기타 설정 법칙")
rules_input = st.text_area("설정 룰 (한 줄에 하나씩)", height=100)
rules = [r.strip() for r in rules_input.split("\n") if r.strip()]

# --- 저장
st.markdown("---")
if st.button("💾 세계관 JSON 저장"):
    output = {
        "title": title,
        "description": description,
        "characters": st.session_state.characters,
        "locations": st.session_state.locations,
        "magic_systems": st.session_state.magic_systems,
        "rules": rules,
    }

    os.makedirs("worlds", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"worlds/{title or 'world'}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    st.success(f"✅ 저장 완료! → `{filename}`")

