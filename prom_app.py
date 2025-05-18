from flask import Flask, request, jsonify
import json
import os
from threading import Lock

app = Flask(__name__)
TARGETS_FILE = '/etc/prometheus/targets/targets/targets.json'
lock = Lock()

# Ensure targets file exists
if not os.path.exists(TARGETS_FILE):
    with open(TARGETS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/add_target', methods=['POST'])
def add_target():
    data = request.get_json()
    target = data.get('target')  # e.g. "192.168.1.10:9100"
    labels = data.get('labels', {})  # Optional labels

    if not target:
        return jsonify({"error": "Missing 'target' field"}), 400

    new_entry = {
        "targets": [target],
        "labels": labels
    }

    with lock:
        with open(TARGETS_FILE, 'r+') as f:
            current = json.load(f)
            current.append(new_entry)
            f.seek(0)
            json.dump(current, f, indent=2)
            f.truncate()

    return jsonify({"status": "success", "added": new_entry})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)