# ================================
# IMPORTS
# ================================
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import json
import requests

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from deep_translator import GoogleTranslator

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ================================
# LOAD MODEL + CLASSES
# ================================
model = tf.keras.models.load_model("model/skin_model.h5")

with open("model/classes.json") as f:
    classes = json.load(f)

# ================================
# INIT APP
# ================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# MEMORY (LIMITED)
# ================================
chat_history = []

# ================================
# TRANSLATION
# ================================
def translate(text, lang):
    if lang == "en":
        return text
    try:
        return GoogleTranslator(source="auto", target=lang).translate(text)
    except:
        return text

# ================================
# TREATMENT DATABASE
# ================================
treatment_db = {
    "Acne": ["Low", "Use salicylic acid facewash.", "Avoid oily food."],
    "Eczema": ["Medium", "Use moisturizer & hydrocortisone.", "Avoid harsh soaps."],
    "Psoriasis": ["Medium", "Apply vitamin D ointments.", "Keep skin hydrated."],
    "Skin_Cancer": ["High", "Immediate medical attention required.", "Consult dermatologist urgently."],
    "Fungal_Infection": ["Low", "Use antifungal creams.", "Keep skin dry."],
    "Bacterial_Infection": ["Medium", "Use antibiotics if prescribed.", "Maintain hygiene."],
    "Viral_Infection": ["Medium", "Avoid contact, use antiviral meds.", "Keep area clean."],
    "Normal": ["Low", "No treatment needed.", "Maintain skincare."]
}

# ================================
# IMAGE PREDICTION
# ================================
@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...), language: str = "en"):
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
        image = image.resize((224, 224))

        img = np.array(image) / 255.0
        img = np.expand_dims(img, axis=0)

        preds = model.predict(img)[0]
        top_indices = preds.argsort()[-3:][::-1]

        results = [
            {
                "disease": translate(classes[i], language),
                "confidence": round(float(preds[i]) * 100, 2)
            }
            for i in top_indices
        ]

        main = classes[top_indices[0]]
        risk, treatment, advice = treatment_db.get(main, ["Unknown", "Consult doctor", "No advice"])

        return {
            "predictions": results,
            "risk": translate(risk, language),
            "treatment": translate(treatment, language),
            "advice": translate(advice, language)
        }

    except Exception as e:
        return {"error": str(e)}

# ================================
# SYMPTOM CHECKER
# ================================
class SymptomRequest(BaseModel):
    symptom1: str | None = None
    symptom2: str | None = None
    language: str = "en"

@app.post("/predict/symptoms")
async def predict_symptoms(req: SymptomRequest):

    text = f"{req.symptom1 or ''} {req.symptom2 or ''}".lower()

    scores = {
        "Acne": 0,
        "Eczema": 0,
        "Psoriasis": 0,
        "Fungal_Infection": 0,
        "Bacterial_Infection": 0,
        "Viral_Infection": 0
    }

    if any(x in text for x in ["pimple", "acne", "oil"]):
        scores["Acne"] += 2
    if any(x in text for x in ["itch", "dry", "rash"]):
        scores["Eczema"] += 2
    if any(x in text for x in ["red", "patch", "scaling"]):
        scores["Psoriasis"] += 2
    if any(x in text for x in ["ring", "circle"]):
        scores["Fungal_Infection"] += 2
    if any(x in text for x in ["pus", "swelling", "pain"]):
        scores["Bacterial_Infection"] += 2
    if any(x in text for x in ["blister", "spread"]):
        scores["Viral_Infection"] += 2

    disease = max(scores, key=scores.get)

    if scores[disease] == 0:
        disease = "Normal"
        confidence = 50
    else:
        confidence = min(70 + scores[disease]*5, 95)

    risk, treatment, advice = treatment_db[disease]

    return {
        "disease": translate(disease, req.language),
        "confidence": confidence,
        "risk": translate(risk, req.language),
        "treatment": translate(treatment, req.language),
        "advice": translate(advice, req.language)
    }

# ================================
# CHATBOT (OLLAMA OPTIMIZED)
# ================================
class ChatRequest(BaseModel):
    msg: str
    language: str = "en"

@app.post("/chat")
async def chat(req: ChatRequest):

    global chat_history

    try:
        chat_history.append({"role": "user", "content": req.msg})
        chat_history = chat_history[-6:]

        context = "\n".join([m["content"] for m in chat_history])

        prompt = f"""
You are a professional dermatology assistant.

Conversation:
{context}

Rules:
- Max 6 lines
- Bullet points only
- No long paragraphs
- Clear and readable
- Suggest doctor if serious

Format:
• What it is
• Causes
• Treatment
• When to worry
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 300,
                    "temperature": 0.5
                }
            },
            timeout=25
        )

        reply = response.json().get("response", "").strip()

        reply = "\n".join(line.strip() for line in reply.split("\n") if line.strip())

        chat_history.append({"role": "assistant", "content": reply})

        if not reply:
            raise Exception("Empty response")

    except Exception as e:
        print("🔥 OLLAMA ERROR:", e)
        reply = "AI is busy. Please try again."

    return {"response": translate(reply, req.language)}

# ================================
# PDF REPORT (DOWNLOAD FIXED)
# ================================
@app.post("/generate-report")
async def generate_report(data: dict):

    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Skin Disease Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Disease: {data.get('disease')}", styles["Normal"]))
    content.append(Paragraph(f"Confidence: {data.get('confidence')}%", styles["Normal"]))
    content.append(Paragraph(f"Risk Level: {data.get('risk')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Treatment: {data.get('treatment')}", styles["Normal"]))
    content.append(Paragraph(f"Advice: {data.get('advice')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("⚠ AI-generated report. Consult a doctor.", styles["Normal"]))

    doc.build(content)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="skin_report.pdf"
    )

# ================================
# ROOT
# ================================
@app.get("/")
def home():
    return {"status": "Backend running"}