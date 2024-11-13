from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import subprocess
import traceback
import re

ffmpeg_path = r"C:\Users\DELL\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://d182-105-112-125-236.ngrok-free.app"]}})

DOWNLOAD_FOLDER = os.path.abspath('downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]+', '', filename.encode("ascii", "ignore").decode())

def download_video_helper(video_url, user_chosen_directory):
    """Download video and return file path and sanitized title."""
    try:
        output_path = os.path.join(user_chosen_directory, '%(title)s.%(ext)s')
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = sanitize_filename(info_dict.get('title', 'video'))
            return os.path.join(user_chosen_directory, f"{title}.mp4"), title
    except Exception as e:
        print(f"Error in download_video_helper: {e}")
        raise

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format', 'mp4')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    file_path = None  # Initialize file_path

    try:
        # Call helper to download video
        video_path, title = download_video_helper(url, DOWNLOAD_FOLDER)

        if format_type == 'mp3':
            audio_path = os.path.join(DOWNLOAD_FOLDER, f"{title}.mp3")
            conversion_command = [
                ffmpeg_path,
                '-i', video_path,
                '-q:a', '0', '-map', 'a',
                audio_path
            ]

            try:
                subprocess.run(conversion_command, check=True)
                file_path = audio_path
            except subprocess.CalledProcessError as e:
                print(f"Error during audio conversion: {e}")
                return jsonify({"error": "Audio conversion failed"}), 500
        else:
            file_path = video_path

        if os.path.exists(file_path):
            return send_file(
                file_path, 
                as_attachment=True, 
                download_name=f"{title}.{format_type}", 
                mimetype=f"audio/{format_type}" if format_type == "mp3" else "video/mp4"
            )
        else:
            return jsonify({"error": "File not found after download"}), 404

    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({"error": f"Server error: {str(e)}"}), 500

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except Exception as cleanup_error:
                print(f"Failed to remove file {file_path}: {str(cleanup_error)}")

if __name__ == "__main__":
    app.run(debug=True)
