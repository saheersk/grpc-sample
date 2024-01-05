import os
import requests

from flask import Flask, jsonify, request
from asgiref.wsgi import WsgiToAsgi


app = Flask(__name__)

TASK_URL = "http://task-app:8000/task/api/v1/service/"

items = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
    {'id': 3, 'name': 'Item 3'},
]


@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/task/', methods=['GET', 'POST'])
def gateway_task():
    method = request.method
    data = request.json if method == 'POST' else None

    try:
        response = make_task_request(method, data)
        return jsonify(response)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

def make_task_request(method, data=None):
    headers = {'Content-Type': 'application/json'}

    if method == 'GET':
        response = requests.get(TASK_URL, headers=headers)
    elif method == 'POST':
        response = requests.post(TASK_URL, json=data, headers=headers)
    else:
        raise requests.exceptions.RequestException("Method Not Allowed")

    response.raise_for_status()
    return response.json()


asgi_handler = WsgiToAsgi(app)

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        import uvicorn
        uvicorn.run(asgi_handler, host='0.0.0.0', port=8000)