from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # CORS import edilir
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # CORS izinlerini ekliyoruz

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # YouTube video URL'sinden video dosyasını indirme işlemi
        ydl_opts = {
            'format': 'best',  # En iyi formatı seçer
            'outtmpl': 'video.mp4',  # İndirilen video 'video.mp4' olarak kaydedilir
            'quiet': True,  # Logları gizler
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Video indirildikten sonra dosyayı gönder
        return send_file('video.mp4', as_attachment=True, download_name='video.mp4')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
