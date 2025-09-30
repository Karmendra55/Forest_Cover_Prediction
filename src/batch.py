import streamlit as st
import pandas as pd
from utils.model import load_model
from datetime import datetime
import numpy as np
from pathlib import Path
from utils.viz import (
        plot_batch_bar_chart,
        plot_batch_pie_chart,
        plot_feature_boxplots,
    )
from utils.template import get_csv_template
from utils.theme import apply_batch_styles
from src.history import save_to_history

# --- Caching ---
@st.cache_resource
def load_model_cached(path):
    return load_model(path)

@st.cache_data
def get_cached_template():
    return get_csv_template()

apply_batch_styles()

model = load_model_cached("model/xgb_model.pkl")
SAVE_ROOT = Path("Saved_Predictions")

cover_type_map = {
        1: "Spruce/Fir",
        2: "Lodgepole Pine",
        3: "Ponderosa Pine",
        4: "Cottonwood/Willow",
        5: "Aspen",
        6: "Douglas-fir",
        7: "Krummholz",
    }

def show():
    st.subheader("📄 Batch Prediction")
    
    with st.expander("📥 Download CSV Template"):
        st.markdown("Use this template to format your dataset properly before uploading.")

        n_rows = st.slider("Number of template rows", 0, 30, 3, key="template_rows")

        template_df = get_csv_template(n_rows=n_rows, use_random=True)
        template_csv = template_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="⬇️",
            data=template_csv,
            file_name="forest_cover_template.csv",
            mime="text/csv",
            help="Download a CSV with the correct columns and example rows."
        )

        st.dataframe(template_df, use_container_width=True)
    
    uploaded_file = st.file_uploader(
        "📂 Upload your dataset (CSV)", 
        type=["csv"], 
        key="batch_upload",
        help="Upload a properly formatted CSV file.",
    )

    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            data = pd.read_csv(uploaded_file)
            if data.empty:
                st.warning("⚠️ The uploaded CSV file is empty.")
                return

            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.markdown("<div class='custom-title'>📊 Uploaded Data Preview</div>", unsafe_allow_html=True)
            st.dataframe(data.head(), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Prediction Button ---
            if st.button("Predict Cover Types"):
                feature_columns = model.get_booster().feature_names
                missing_cols = set(feature_columns) - set(data.columns)
                
                if missing_cols:
                    st.error(f"❌ Uploaded file is missing columns: {', '.join(sorted(missing_cols))}")
                    st.stop()
                else:
                    data = data[feature_columns].copy()
                    soil_cols = [col for col in data.columns if col.startswith("Soil_Type")]
                    wilderness_cols = [col for col in data.columns if col.startswith("Wilderness_Area")]

                    # --- Validate soil ---
                    invalid_soil_rows = data[soil_cols].sum(axis=1) != 1
                    if invalid_soil_rows.any():
                        bad_indices = data.index[invalid_soil_rows].tolist()
                        st.error("❌ Invalid Soil_Type encoding detected!")
                        st.warning(
                            f"- Each row must have exactly 1 value = 1 across {len(soil_cols)} Soil_Type columns.\n"
                            f"- Found {len(bad_indices)} invalid rows (showing first 10): {bad_indices[:10]}"
                        )
                        st.stop()

                    # --- Validate wilderness ---
                    invalid_wild_rows = data[wilderness_cols].sum(axis=1) != 1
                    if invalid_wild_rows.any():
                        bad_indices = data.index[invalid_wild_rows].tolist()
                        st.error("❌ Invalid Wilderness_Area encoding detected!")
                        st.warning(
                            f"- Each row must have exactly 1 value = 1 across {len(wilderness_cols)} Wilderness_Area columns.\n"
                            f"- Found {len(bad_indices)} invalid rows (showing first 5): {bad_indices[:5]}"
                        )
                        st.stop()

                # --- Prediction ---
                try:
                    with st.spinner("🔄 Predicting Cover Types..."):
                        predictions = model.predict(data).astype(int) + 1
                        predicted_classes = [cover_type_map.get(int(i), "Unknown") for i in predictions]
                except Exception as e:
                    st.error(f"❌ Prediction failed: {e}")
                    return

                data["Predicted_Cover_Type_Number"] = predictions
                data["Predicted_Cover_Type_Name"] = predicted_classes

                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='custom-title'>✅ Prediction Completed!</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<div class='custom-sub'>Your dataset has been successfully processed "
                    "and predictions have been added.</div>",
                    unsafe_allow_html=True,
                )
                st.dataframe(data.head(), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_dir = SAVE_ROOT / "batch" / timestamp
                save_dir.mkdir(parents=True, exist_ok=True)
                
                csv_path = save_dir / "predictions.csv"
                data.to_csv(csv_path, index=False, encoding="utf-8")

                # --- Visualizations
                viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart", "📦 Boxplots"])

                with viz_tab1:
                    try:
                        fig_bar = plot_batch_bar_chart(predictions, cover_type_map, save_path=save_dir / "bar.png")
                        if fig_bar is not None:
                            st.plotly_chart(fig_bar, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not render/save bar chart: {e}")

                # Pie chart
                with viz_tab2:
                    try:
                        fig_pie = plot_batch_pie_chart(predictions, cover_type_map, save_path=save_dir / "pie.png")
                        if fig_pie is not None:
                            st.plotly_chart(fig_pie, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not render/save pie chart: {e}")

                with viz_tab3:
                    try:
                        fig_box = plot_feature_boxplots(data, predictions, cover_type_map, save_path=save_dir / "box.png")
                        try:
                            import matplotlib.pyplot as plt
                            if fig_box is not None:
                                st.pyplot(fig_box)
                        except Exception:
                            pass
                    except Exception as e:
                        st.warning(f"Could not render/save feature boxplots: {e}")
                
                try:
                    save_to_history("batch", {
                        "file": uploaded_file.name,
                        "rows": int(len(data)),
                        "path": str(save_dir),
                        "predictions_preview": (predictions[:10].tolist() if hasattr(predictions, "tolist") else list(predictions)[:10])
                    })
                    st.success("The Records have been saved successfully and are available in History → Batch.")
                except Exception as e:
                    st.error(f"⚠️ Failed to save batch history: {e}")

        except pd.errors.EmptyDataError:
            st.error("❌ The uploaded file is empty or not a valid CSV.")
        except pd.errors.ParserError:
            st.error("❌ Failed to parse CSV. Please check your file format.")
        except UnicodeDecodeError:
            st.error("❌ File encoding not supported. Please upload a UTF-8 encoded CSV.")
        except Exception as e:
            st.error(f"❌ Unexpected error while reading the file: {str(e)}")