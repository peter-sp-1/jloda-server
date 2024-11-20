from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import subprocess
from threading import Timer
import webbrowser
import requests

app = Flask(__name__)
# Configure CORS to allow requests from any origin
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://jloda.vercel.app",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "YouTube Downloader API is running", "status": "active"})

DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in (' ', '-', '_', '.') else '_' for c in filename)

@app.route('/download', methods=['POST', 'OPTIONS'])
def download_video():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})

    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400

        url = data['url']
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        if not os.path.exists(file_path):
            return jsonify({'error': 'Download failed'}), 500

        output_filename = sanitize_filename(os.path.splitext(os.path.basename(file_path))[0] + '.mp3')
        output_path = os.path.join(DOWNLOAD_DIR, output_filename)

        conversion_command = [
            'ffmpeg',
            '-i', file_path,
            '-q:a', '0',
            '-map', 'a',
            output_path
        ]

        subprocess.run(conversion_command, check=True, capture_output=True, text=True)

        try:
            os.remove(file_path)
        except OSError:
            pass

        if os.path.exists(output_path):
            response = send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='audio/mpeg'
            )
            # Add CORS headers to the file response
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return jsonify({'error': 'Conversion failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_ngrok_url():
    try:
        # Get the ngrok tunnel information
        response = requests.get('https://8191-102-89-32-248.ngrok-free.app')
        tunnels = response.json()['tunnels']
        # Find the HTTPS tunnel
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except:
        return None

if __name__ == '__main__':
    # Start Flask app
    app.run(debug=True)
