import numpy as np
import pandas as pd
import re
from utils.model import load_model

def prepare_input_data(user_inputs):
    input_data = np.zeros((1, 54))
    input_data[0, 0] = user_inputs["elevation"]
    input_data[0, 1] = user_inputs["aspect"]
    input_data[0, 2] = user_inputs["slope"]
    input_data[0, 3] = user_inputs["horz_dist_hydro"]
    input_data[0, 4] = user_inputs["vert_dist_hydro"]
    input_data[0, 5] = user_inputs["horz_dist_road"]
    input_data[0, 6] = user_inputs["hillshade_9am"]
    input_data[0, 7] = user_inputs["hillshade_noon"]
    input_data[0, 8] = user_inputs["hillshade_3pm"]
    input_data[0, 9] = user_inputs["horz_dist_fire"]

    wa_index = int(re.findall(r'\d+', user_inputs["wilderness_area"])[0]) - 1
    input_data[0, 10 + wa_index] = 1

    st_index = int(re.findall(r'\d+', user_inputs["soil_type"])[0]) - 1
    input_data[0, 14 + st_index] = 1

    return input_data

def validate_csv(data, st):
    expected_cols = 54
    model = load_model("model/xgb_model.pkl")
    expected_columns = model.get_booster().feature_names
    
    if not list(data.columns) == expected_columns:
        st.error("❌ Column names or order mismatch with the trained model features.")
        return False
    if data.shape[1] != expected_cols:
        st.error(f"❌ Uploaded file must have exactly {expected_cols} features, found {data.shape[1]}.")
        return False
    if data.isnull().values.any():
        st.error("❌ Uploaded file contains missing values. Please clean the data.")
        return False
    return True

def load_processed_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load processed data: {e}")
