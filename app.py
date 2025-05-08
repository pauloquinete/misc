from flask import Flask, jsonify
import socket
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def info():
  hostname = socket.gethostname()
  current_time = datetime.now().isoformat()
  return jsonify({
    'hostname': hostname,
    'date': current_time
    })

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
