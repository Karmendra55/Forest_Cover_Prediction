import pickle
from utils.logger import log_error

def load_model(model_path):
    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        log_error("Failed to load model", e)
        raise

def predict_cover_type(model, input_data):
    try:
        predicted_class = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        return predicted_class, probabilities
    except Exception as e:
        log_error("Prediction failed", e)
        raise

def get_cover_type_name(class_id, cover_type_map):
    return cover_type_map.get(class_id, "Unknown")
