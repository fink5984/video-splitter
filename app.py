from flask import Flask, request, jsonify
import requests
from PIL import Image
import pytesseract
from io import BytesIO

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # קבלת ה-URL של התמונה מהבקשה
        image_url = request.json.get('url')
        if not image_url:
            return jsonify({"error": "URL is required"}), 400

        # הורדת התמונה
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch image from URL"}), 400

        # פתיחת התמונה ופענוח הטקסט
        image = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(image, lang='heb+eng')  # תמיכה בעברית ואנגלית

        return jsonify({"text": text.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
