from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/render', methods=['POST'])
def render_video():
    data = request.json
    input_url = data.get('video_url')

    if not input_url:
        return jsonify({"status": "error", "message": "Thiếu tham số video_url"}), 400

    output_file = "output.mp4"

    # Lệnh FFmpeg xử lý video
    command = f"ffmpeg -i {input_url} -c:v copy {output_file}"

    # Chạy lệnh FFmpeg trên hệ thống
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    if process.returncode == 0:
        return jsonify({
            "status": "success", 
            "message": "Render video thành công!",
            "output": output_file
        })
    else:
        return jsonify({
            "status": "error", 
            "message": "Lỗi khi chạy FFmpeg", 
            "detail": process.stderr
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
