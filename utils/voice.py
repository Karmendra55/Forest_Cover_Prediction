import streamlit as st
from streamlit.components.v1 import html
import base64
import os
from utils.logger import log_error

def add_intro_voice(audio_file_path: str) -> None:
    if not os.path.exists(audio_file_path):
        log_error("Audio file not found", audio_file_path)
        st.warning("⚠️ Intro audio file is missing.")
        return
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #0dcaf0;
            color: #1e1e1e;
            border-radius: 6px;
            padding: 6px 14px;
            font-size: 14px;
            font-weight: 500;
            border: none;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #0bb2d4;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        encoded_audio = base64.b64encode(audio_bytes).decode()
    except Exception as e:
        log_error("Failed to load audio file", e)
        st.warning("⚠️ Could not load intro audio.")
        return

    if st.button("▶️ Play Intro Brief"):
        try:
            html(
                f"""
                <script>
                    var audio = new Audio("data:audio/mp3;base64,{encoded_audio}");
                    audio.play();
                </script>
                """,
                height=0,
            )
        except Exception as e:
            log_error("Failed to play intro audio", e)
            st.audio(audio_bytes, format="audio/mp3")