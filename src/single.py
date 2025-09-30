import streamlit as st
from pathlib import Path
import json, numpy as np, pandas as pd
from utils.model import load_model, predict_cover_type
from utils.data import prepare_input_data
from datetime import datetime
from utils.pdf import generate_single_patch_pdf
from utils.viz import (
    plot_prediction_probabilities,
    plot_probability_radar_chart,
    plot_patch_grid,
)
from utils.randomizer import randomize_inputs
from utils.theme import apply_global_styles 
from src.history import save_to_history

apply_global_styles()

@st.cache_resource(show_spinner="Loading prediction model...")
def load_model_cached(path: str):
    try:
        return load_model(path)
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        st.stop()

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

def sanitize(obj):
    if isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    if isinstance(obj, (np.ndarray, list)):
        return [sanitize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    return obj

# --------------
# Input Form
# --------------
def get_user_input():
    st.subheader("🌱 Predict for a Single Patch")
    st.markdown("Enter terrain properties below to predict vegetation cover type.")

    # Randomize button
    if st.button("🎲 Randomize Inputs"):
        random_values = randomize_inputs()
        for key, value in random_values.items():
            st.session_state[key] = value
    with st.form("single_patch_form"):
        st.subheader("⛰️ Terrain Properties")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.slider("Elevation (meters)", 1500, 4500, value=2500, key="elevation",
                      help="🌄 *Elevation*: Vertical distance above sea level (in meters). Higher elevations may indicate alpine vegetation.")
        with col2:
            st.slider("Aspect (degrees)", 0, 360, value=180, key="aspect",
                      help="🧭 *Aspect*: Compass direction that a slope faces (0 = North, 90 = East). Affects sunlight exposure.")
        with col3:
            st.slider("Slope (degrees)", 0, 75, value=30, key="slope",
                      help="⛰️ *Slope*: Steepness of terrain (in degrees). Flat = 0°, Steep = 60°.")

        st.subheader("💧 Hydrology Distances")
        col4, col5 = st.columns(2)
        with col4:
            st.number_input("Horizontal Distance to Hydrology (Works best: 0-2000 m)", value=250, key="horz_dist_hydro",
                            help="💧 *Horizontal distance* (in meters) to the nearest water body like rivers, lakes, or streams.")
        with col5:
            st.number_input("Vertical Distance to Hydrology (Works best: (-200) to 800 m)", value=100, key="vert_dist_hydro",
                            help="💧 *Vertical distance* (in meters) above or below the nearest water body. Negative = below water level.")

        st.subheader("🛣️ Infrastructure Distances")
        col6, col7 = st.columns(2)
        with col6:
            st.number_input("Horizontal Distance to Roadways (Works best: 0-8000 m)", value=600, key="horz_dist_road",
                            help="🛣️ *Distance* (in meters) to the nearest road. Lower values mean closer proximity.")
        with col7:
            st.number_input("Horizontal Distance to Fire Points (Works best: 0-8000 m)", value=800, key="horz_dist_fire",
                            help="🔥 *Distance* (in meters) to the nearest wildfire ignition point. Affects vegetation recovery.")

        st.subheader("🌞 Hillshade Values")
        col8, col9, col10 = st.columns(3)
        with col8:
            st.slider("Hillshade at 9am", 0, 255, value=124, key="hillshade_9am",
                      help="🌞 *Hillshade* value (0–255) representing sunlight at 9 AM. 0 -> darkest, 255 -> brightest.")
        with col9:
            st.slider("Hillshade at Noon", 0, 255, value=124, key="hillshade_noon",
                      help="🌞 *Hillshade* value (0–255) representing sunlight at noon. Used to model sun exposure.")
        with col10:
            st.slider("Hillshade at 3pm", 0, 255, value=124, key="hillshade_3pm",
                      help="🌞 *Hillshade* value (0–255) representing sunlight at 3 PM.")

        st.subheader("🏞️ Environmental Categories")
        col11, col12 = st.columns(2)
        with col11:
            st.selectbox("Wilderness Area",
                         ["Wilderness_Area1", "Wilderness_Area2", "Wilderness_Area3", "Wilderness_Area4"],
                         key="wilderness_area",
                         help="🏞️ *Wilderness Area*: Categorical zone (1–4) in the study area.")
        with col12:
            st.selectbox("Soil Type", [f"Soil_Type{i}" for i in range(1, 41)],
                         key="soil_type",
                         help="🌱 *Soil Type*: Categorical soil classification (1–40). Affects vegetation and drainage.")

        # --- Submit button ---
        submitted = st.form_submit_button("🔍 Predict")
        if not submitted:
            return None

        if submitted:
            user_inputs = {
                "elevation": st.session_state["elevation"],
                "aspect": st.session_state["aspect"],
                "slope": st.session_state["slope"],
                "horz_dist_hydro": st.session_state["horz_dist_hydro"],
                "vert_dist_hydro": st.session_state["vert_dist_hydro"],
                "horz_dist_road": st.session_state["horz_dist_road"],
                "horz_dist_fire": st.session_state["horz_dist_fire"],
                "hillshade_9am": st.session_state["hillshade_9am"],
                "hillshade_noon": st.session_state["hillshade_noon"],
                "hillshade_3pm": st.session_state["hillshade_3pm"],
                "wilderness_area": st.session_state["wilderness_area"],
                "soil_type": st.session_state["soil_type"],
            }

            if user_inputs["vert_dist_hydro"] > user_inputs["horz_dist_hydro"]:
                st.warning("⚠️ Vertical Distance to Hydrology is unusually high compared to Horizontal Distance.")
            return user_inputs

def make_prediction(inputs: dict):
    with st.spinner("Predicting Cover Type..."):
        input_data = prepare_input_data(inputs)
        predicted_class, probabilities = predict_cover_type(model, input_data)
        predicted_class += 1 
        return predicted_class, probabilities
            
def display_results(pred_class, probs, user_inputs):
    """Show prediction results, charts, and export option."""  
    predicted_name = cover_type_map.get(pred_class, "Unknown")
    confidence = max(probs) * 100
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ------------------------
    # Auto-save to history
    # ------------------------
    save_dir = SAVE_ROOT / "single" / timestamp
    save_dir.mkdir(parents=True, exist_ok=True)

    record = sanitize({
        "timestamp": timestamp,
        "prediction": int(pred_class),
        "prediction_name": predicted_name,
        "confidence": confidence,
        "probabilities": probs.tolist() if hasattr(probs, "tolist") else probs,
        "inputs": user_inputs,
        "path": str(save_dir),
    })

    with open(save_dir / "prediction.json", "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    if confidence > 95:
        emoji, tooltip = "🏆", "Extremely Confident"
    elif confidence > 85:
        emoji, tooltip = "🌟", "Very Confident"
    elif confidence > 70:
        emoji, tooltip = "✅", "Confident"
    elif confidence > 50:
        emoji, tooltip = "⚠️", "Low Confidence"
    else:
        emoji, tooltip = "❌", "Very Low Confidence"

    # -------------------
    # Prediction Card
    # -------------------
    with st.container():
        st.markdown(
            f"<div class='result-card'>"
            f"<div class='result-title'>🌲 Predicted Cover Type: <b>{predicted_name}</b></div>"
            f"<div class='confidence'>Prediction Confidence: <b>{confidence:.2f}%</b>"
            f"<span title='{tooltip}'>{emoji}</span></div>"
            f"</div>",
            unsafe_allow_html=True,
        )
             
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📊 Radar Chart", "🟩 Grid Chart", "📦 Probability Barplot"])       
    with viz_tab1:
        _,col2,_ = st.columns([1,3,1])
        with col2:    
            radar_chart = plot_probability_radar_chart(probs, cover_type_map, save_path=save_dir / "radar.png")
    with viz_tab2:
        _,col2,_ = st.columns([1,2,1])
        with col2:    
            grid_chart  = plot_patch_grid(probs, cover_type_map, save_path=save_dir / "grid.png")
    with viz_tab3:
        plot_prediction_probabilities(probs, cover_type_map, save_path=save_dir / "bar.png")

    try:        
        charts_paths = [
            str(save_dir / "radar.png"),
            str(save_dir / "grid.png"),
            str(save_dir / "bar.png"),
        ]
        pdf_bytes = generate_single_patch_pdf(
            user_inputs=user_inputs,
            predicted_class=pred_class,
            predicted_name=predicted_name,
            probabilities=record["probabilities"],
            cover_type_map=cover_type_map,
            charts=charts_paths,
        )
        with open(save_dir / "prediction.pdf", "wb") as f:
            f.write(pdf_bytes)

        save_to_history("single", {
            "timestamp": timestamp,
            "path": str(save_dir),
            "prediction": int(pred_class),
            "prediction_name": predicted_name,
            "confidence": confidence,
            "probabilities": record["probabilities"],
            "inputs": user_inputs,
        })
                
        st.success("The Record has been saved successfully!")
    except Exception as e:
        st.error(f"The Generation can not be saved. ({e})")
                
def show():

    user_inputs = get_user_input()

    if user_inputs:
        with st.spinner("Running prediction..."):
            pred_class, probs = make_prediction(user_inputs)
            display_results(pred_class, probs, user_inputs)