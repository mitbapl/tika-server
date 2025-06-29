from flask import Flask, request, jsonify
import subprocess, uuid, os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400

    file = request.files['file']
    filename = f"/tmp/{uuid.uuid4()}.pdf"
    file.save(filename)

    try:
        result = subprocess.run(["java", "-jar", "tika-app.jar", "-t", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        os.remove(filename)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
        return jsonify({'text': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 9998))
    app.run(host="0.0.0.0", port=port)
