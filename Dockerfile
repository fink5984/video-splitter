# 1. השתמש בתמונה בסיסית של Python (גרסה 3.9 לדוגמה)
FROM python:3.9-slim

# 2. עדכון והתקנת Tesseract ודרישות נוספות
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    tesseract-ocr-heb && \
    apt-get clean

# 3. העתק את קובץ ה-requirements.txt שלך ל-Docker container
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# 4. התקנת כל התלויות מ-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. העתק את שאר הקבצים לתוך ה-container
COPY . /app

# 6. חשוף את הפורט שהאפליקציה שלך תרוץ עליו (בדרך כלל 5000 לפלאסק)
EXPOSE 5000

# 7. הפעל את האפליקציה שלך
CMD ["python", "app.py"]
