from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    # Generate a unique filename so requests don't overwrite each other
    file_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': output_template,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # prepare_filename may return the pre-merge name; force .mp4
            filename = os.path.splitext(filename)[0] + ".mp4"

        return jsonify({
            "status": "success",
            "download_url": f"/downloads/{os.path.basename(filename)}",
            "title": info.get("title")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/downloads/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)