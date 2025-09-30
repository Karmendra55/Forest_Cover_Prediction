import streamlit as st
import time
from utils.logger import log_error

st.set_page_config(
    page_title="Forest Cover Prediction",
    page_icon="🌲",
    layout="wide"
)

# --- Loading modules ---
try:
    from src import (
        about, batch, single, model_loader, sidebar, spinner, history, dataset
    )
    from utils.theme import home_style, apply_theme
    from utils.theme import themed_divider
except Exception as e:
    log_error("Module import failed", e)
    st.stop()

home_style()

# --- Title & Description ---
st.title("🌳 Forest Cover Type Prediction System")
st.caption("Easily find the patterns of The tree types in different Parameters and different Entries.")
themed_divider()

# --- Theme state ---
if "theme" not in st.session_state: 
    try: 
        st.session_state["theme"] = sidebar.load_theme().lower()
    except Exception: 
        st.session_state["theme"] = "default"

apply_theme(st.session_state["theme"])

# --- Sidebar ---
with st.sidebar:
    sidebar.render_sidebar()

# --- Model Loading ---
with st.spinner("🔄 Loading model and preparing environment..."):
    time.sleep(1)
    try:
        model = model_loader.load_model_cached("model/xgb_model.pkl")
    except Exception as e:
        log_error("Model loading failed", e)
        model = None

spinner.handle_spinner()

# --- Page Routing ---
try:
    if st.session_state.active_tab == "About":
        about.show()
    elif st.session_state.active_tab == "Dataset Preview":
        dataset.show()
    elif st.session_state.active_tab == "Single Patch Prediction":
        single.show()
    elif st.session_state.active_tab == "Batch Prediction":
        batch.show()
    elif st.session_state.active_tab == "History":
        history.show()
    else:
        st.info("ℹ️ Please select a section from the sidebar.")
except Exception as e:
    log_error("An error occurred while rendering this page", e)

# --- Footer ---
themed_divider()
st.markdown(
    """
    <div class="footer">
        Developed with ❤️ by <b>Karmendra Srivastava</b> | Trained in Jupyter Notebook
    </div>
    """,
    unsafe_allow_html=True
)