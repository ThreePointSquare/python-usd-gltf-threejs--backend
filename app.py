from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/execute', methods=['POST'])
def execute():
    code = request.json['code']
    script_path = os.path.join(UPLOAD_FOLDER, "user_script.py")
    gltf_path = os.path.join(UPLOAD_FOLDER, "output.gltf")

    # Save user code to a script
    with open(script_path, "w") as script_file:
        script_file.write(code)

    # Execute user code and generate glTF
    try:
        subprocess.run(["python", script_path], check=True)
        return jsonify({"gltf_url": f"/static/{os.path.basename(gltf_path)}"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)