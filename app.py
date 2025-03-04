from flask import Flask, render_template, request, jsonify
import requests
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# Google Translate API Key (Replace with your actual API key)
GOOGLE_TRANSLATE_API_KEY = "AIzaSyBGkFWBst1zLNTk4RoJn1cfkcdqfyN_FR4"
GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

# Translate text using Google Translate API
def translate_text(text, source_lang, target_lang):
    params = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "key": GOOGLE_TRANSLATE_API_KEY,
    }
    response = requests.post(GOOGLE_TRANSLATE_URL, params=params)
    if response.status_code == 200:
        return response.json()["data"]["translations"][0]["translatedText"]
    return None

# Extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        return str(e)

# API endpoint for text translation
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text")
    source_lang = data.get("source_lang")
    target_lang = data.get("target_lang")

    if not text or not source_lang or not target_lang:
        return jsonify({"error": "Missing required fields"}), 400

    translated_text = translate_text(text, source_lang, target_lang)
    if translated_text:
        return jsonify({"translated_text": translated_text})
    return jsonify({"error": "Translation failed"}), 500

# API endpoint for OCR
@app.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    image_path = "uploaded_image.png"
    image_file.save(image_path)

    extracted_text = extract_text_from_image(image_path)
    os.remove(image_path)  # Remove the saved image after processing

    return jsonify({"extracted_text": extracted_text})

# Serve the frontend HTML page
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)