import streamlit as st
import time

def handle_spinner():
    try:
        placeholder = st.empty()
        tab_changed = st.session_state.get("last_tab") != st.session_state.active_tab
        theme_changed = st.session_state.get("last_theme") != st.session_state.theme

        if tab_changed or theme_changed:
            msg = (
                f"🔄 Switching to {st.session_state.active_tab}..."
                if tab_changed
                else f"🎨 Applying {st.session_state.theme} Theme..."
            )
            with placeholder.container():
                with st.spinner(msg):
                    time.sleep(1)

            st.session_state.last_tab = st.session_state.active_tab
            st.session_state.last_theme = st.session_state.theme

        placeholder.empty()

    except Exception as exc:
        st.error(f"⚠️ Spinner failed: {exc}")