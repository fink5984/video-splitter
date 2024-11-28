from flask import Flask, request, jsonify
import os
import moviepy.editor as mp
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/split-video', methods=['POST'])
def split_video():
    video_url = request.json.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    # הורדת הסרטון
    video_filename = download_video(video_url)
    if not video_filename:
        return jsonify({"error": "Failed to download video"}), 500

    # חלוקת הסרטון
    output_links = split_video_into_chunks(video_filename)
    if not output_links:
        return jsonify({"error": "Failed to process video"}), 500

    return jsonify({"parts": output_links})

def download_video(url):
    try:
        import youtube_dl
        ydl_opts = {
            'outtmpl': os.path.join(UPLOAD_FOLDER, '%(id)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def split_video_into_chunks(filepath):
    try:
        video = mp.VideoFileClip(filepath)
        duration = int(video.duration)
        file_id = str(uuid.uuid4())
        part_links = []

        for start_time in range(0, duration, 60):
            end_time = min(start_time + 60, duration)
            part = video.subclip(start_time, end_time)
            output_filename = os.path.join(OUTPUT_FOLDER, f"{file_id}_part_{start_time}.mp4")
            part.write_videofile(output_filename, codec="libx264")
            part_links.append(f"https://your-render-app.com/{output_filename}")

        return part_links
    except Exception as e:
        print(f"Error splitting video: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
