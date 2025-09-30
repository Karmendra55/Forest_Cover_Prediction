import streamlit as st
import os, json, random, time
from utils.theme import apply_theme, themed_divider
from utils.voice import add_intro_voice
from src import about


CACHE_FILE = ".cache/theme.json"

def save_theme(theme_name: str):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump({"theme": theme_name}, f)

def load_theme() -> str:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f).get("theme", "Default")
    return "Default"

def render_sidebar():
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "About"

    # --- Navigation ---
    st.markdown("<h2>⏬ Navigation</h2>", unsafe_allow_html=True)
    st.selectbox(
        "Go to:",
        ["About", "Dataset Preview", "Single Patch Prediction", "Batch Prediction", "History"],
        index=["About", "Dataset Preview", "Single Patch Prediction", "Batch Prediction", "History"].index(
            st.session_state.get("active_tab", "About")
        ),
        key="active_tab"
    )
    themed_divider()

    # --- Theme ---
    st.markdown("<h2>🎨 Theme</h2>", unsafe_allow_html=True)

    theme = st.selectbox(
        "Select Theme",
        options=["Default", "Dark", "Tree"],
        index=["default", "dark", "tree"].index(st.session_state.get("theme", "default")),
        key="theme_select"
    ).lower()

    # --- Only apply/save if changed ---
    if theme != st.session_state.get("theme", "default"):
        st.session_state["theme"] = theme
        apply_theme(theme)
        save_theme(theme)
        st.rerun()

    apply_theme(st.session_state["theme"])

    if st.session_state["theme"] == "tree":
        st.markdown(
            "<small>This Theme is heavy and may cause issues on low-end systems.</small>",
            unsafe_allow_html=True
        )

    themed_divider()

    st.markdown("<h2>🎤 Voice Introduction</h2>", unsafe_allow_html=True)
    add_intro_voice("audio/intro.mp3")
    themed_divider()

    if "sidebar_caption" not in st.session_state:
        st.session_state.sidebar_caption = random.choice(about.captions())
        st.session_state.caption_time = time.time()
    if time.time() - st.session_state.caption_time > 120:
        st.session_state.sidebar_caption = random.choice(about.captions())
        st.session_state.caption_time = time.time()
        st.rerun()
    st.markdown(f"<small>{st.session_state.sidebar_caption}</small>", unsafe_allow_html=True)
    
    themed_divider()