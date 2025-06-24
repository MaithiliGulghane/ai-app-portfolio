import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

# 🔄 Load the trained model
model = tf.keras.models.load_model("cat_vs_dog_cnn.h5")

# 🧾 Class names (based on label 0 = cat, 1 = dog)
class_names = ["Cat", "Dog"]

# 🔍 Preprocessing function
def preprocess_image(img: Image.Image) -> np.ndarray:
    img = img.resize((32, 32))          # Resize to 32x32 (CIFAR size)
    img_array = np.array(img) / 255.0   # Normalize to [0,1]
    
    if img_array.shape[-1] == 4:
        img_array = img_array[..., :3]  # Convert RGBA to RGB if needed

    return np.expand_dims(img_array, axis=0)  # Add batch dimension

# 🧠 Prediction function
def predict_image(image: Image.Image) -> str:
    processed = preprocess_image(image)
    prediction = model.predict(processed)[0][0]
    label = class_names[int(prediction > 0.5)]
    confidence = prediction if prediction > 0.5 else 1 - prediction
    return f"{label} ({confidence * 100:.2f}% confidence)"

# 🎛️ Gradio Interface
interface = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="🐾 Cat vs Dog Classifier (CIFAR-10 CNN)",
    description="Upload an image of a **cat or dog**. The model will predict whether it's a cat 🐱 or a dog 🐶."
)

# 🚀 Launch the app (for local testing)
if __name__ == "__main__":
    interface.launch()
