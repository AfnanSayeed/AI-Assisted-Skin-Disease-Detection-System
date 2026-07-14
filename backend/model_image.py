import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load model
model_path = os.path.join(os.getcwd(), "skin_model.h5")
model = load_model(model_path)

# Class mapping
class_mapping = {0: "acne", 1: "eczema", 2: "melanoma", 3: "normal", 4: "psoriasis"}

def predict_image(img_path):
    # Load image
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    preds = model.predict(img_array)
    class_index = np.argmax(preds[0])
    confidence = float(np.max(preds[0]))

    return {
        "disease": class_mapping[class_index],
        "confidence": round(confidence*100, 2)
    }
