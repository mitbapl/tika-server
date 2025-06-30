from flask import Flask, request, jsonify
import subprocess, uuid, os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Tika Server is running. Use POST /analyze to upload a PDF.", 200

@app.route('/analyze', methods=['POST'])  
def analyze():
    print("Received request at /analyze") 
    if 'file' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400

    file = request.files['file']
    filename = f"/tmp/{uuid.uuid4()}.pdf"
    file.save(filename)

    try:
        result = subprocess.run(["java", "-jar", "tika-app.jar", "-t", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=300)  # 5 minute timeout
        os.remove(filename)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
        return jsonify({'text': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9998))
    app.run(host="0.0.0.0", port=port)
