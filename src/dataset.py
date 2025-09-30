import os, datetime
import pandas as pd
import streamlit as st
from utils.data import load_processed_data

@st.cache_data
def _load_feature_df(path: str) -> pd.DataFrame:
    df = load_processed_data(path)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def show():
    st.subheader("📊 Dataset Preview")

    feature_path = "dataset/new_forest_data.csv"

    try:
        df = _load_feature_df(feature_path)
        if df.empty:
            st.warning("⚠️ Dataset is empty.")
            return

        file_info = os.stat(feature_path)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📄 Rows", f"{df.shape[0]:,}")
        with c2:
            st.metric("🔢 Columns", f"{df.shape[1]}")
        with c3:
            st.metric("💾 Memory", f"{df.memory_usage().sum()/1_048_576:.2f} MB")
        with c4:
            st.metric(
                "🕒 Updated",
                datetime.datetime.fromtimestamp(file_info.st_mtime).strftime("%b %d, %Y"),
            )

        with st.expander("⚙️ Columns & Data Types"):
            dtype_df = pd.DataFrame({
                "Column": df.columns,
                "Data type": df.dtypes.astype(str),
                "Values Count": df.notnull().sum().values
            })
            st.dataframe(dtype_df, use_container_width=True, height=320)

        # --- Data preview ---
        st.markdown("### 👀 Data Preview")
        row_count = st.slider("Rows", 5, df.shape[0], 20, step=5)
        if row_count >= 1000:
            st.warning("The Amount of Rows Selected May Cause Issues with the performance for low-end devices.")
        selected_cols = st.multiselect("Columns", df.columns.tolist(), default=df.columns.tolist()[:10])
        preview_df = df[selected_cols].head(row_count)
        st.dataframe(preview_df, use_container_width=True)

    except FileNotFoundError:
        st.error(f"❌ {feature_path} not found.")
        return
    except Exception as exc:
        st.error(f"⚠️ Failed to load dataset: {exc}")