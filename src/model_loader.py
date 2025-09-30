import streamlit as st
from utils.model import load_model

@st.cache_resource
def load_model_cached(path):
    try:
        return load_model(path)
    except FileNotFoundError:
        st.error(f"❌ Model file not found at `{path}`.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Failed to load model: {e}")
        st.stop()
