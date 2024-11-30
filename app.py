import pytesseract
from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

# מיקום Tesseract ב-Render
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


@app.route('/')
def home():
    return "OCR API is running!"


@app.route('/extract_text', methods=['POST'])
def extract_text():
    # קבלת URL של התמונה מבקשת POST
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "URL is required"}), 400

    # הורדת התמונה מה-URL
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch the image: {str(e)}"}), 500

    # שימוש ב-Tesseract להמיר את התמונה לטקסט
    try:
        text = pytesseract.image_to_string(img, lang='eng+heb')  # תומך באנגלית ועברית
        return jsonify({"text": text}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
