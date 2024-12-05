from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return jsonify({"message": "API is working!"})

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    download_type = data.get('type')
    video_quality = data.get('quality')

    if not video_url:
        return "No URL provided!", 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': video_quality if video_quality != 'best' else 'best',
        }

        if download_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        # Download using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
