import gradio as gr
import joblib
import numpy as np

model = joblib.load("diabetes_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_diabetes(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age):
    input_data = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    return "Positive" if prediction == 1 else "Negative"

app = gr.Interface(
    fn=predict_diabetes,
    inputs=[
        gr.Number(label="Pregnancies"),
        gr.Number(label="Glucose"),
        gr.Number(label="Blood Pressure"),
        gr.Number(label="Skin Thickness"),
        gr.Number(label="Insulin"),
        gr.Number(label="BMI"),
        gr.Number(label="Diabetes Pedigree Function"),
        gr.Number(label="Age")
    ],
    outputs="text"
)

# ✅ DO NOT call launch() on Hugging Face – just define the interface as `app`
