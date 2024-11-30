import requests

# URL של ה-API
url = "https://video-splitter-e1eh.onrender.com/extract_text"

# כתובת ה-URL של התמונה
image_url = "https://cdnj1.com/assets/1089881/inbox/972523413357/1269655897685880.jpeg"

# שליחת בקשה עם ה-URL של התמונה
response = requests.post(url, json={"image_url": image_url})

# הצגת התגובה
print(response.json())  # זה יציג את התוצאה או שגיאה
