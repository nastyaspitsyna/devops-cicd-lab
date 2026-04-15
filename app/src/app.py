import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)

NEW_GREETING_ENABLED = os.getenv('FEATURE_NEW_GREETING', 'false').lower() == 'true'
@app.route('/')
def index():
    return jsonify({
        'service': 'devops-cicd-demo',
        'version': '1.0.0',
        'hostname': socket.gethostname()
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/greeting')
def greeting():
    if NEW_GREETING_ENABLED:
        return jsonify({'message': 'Hello from the new feature!'})
    else:
        return jsonify({'message': 'Hello, world!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)