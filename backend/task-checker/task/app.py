from flask import Flask, jsonify
from asgiref.wsgi import WsgiToAsgi
import os

app = Flask(__name__)


items = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
    {'id': 3, 'name': 'Item 3'},
]


@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})


asgi_handler = WsgiToAsgi(app)

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        import uvicorn
        uvicorn.run(asgi_handler, host='0.0.0.0', port=8000)