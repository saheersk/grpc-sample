import os

from celery import Celery

from flask import Flask, jsonify
from asgiref.wsgi import WsgiToAsgi
from task.celery import make_celery
from task.tasks import consume_kafka_messages


app = Flask(__name__)

app.config.from_object('task-checker.config')

# Create Celery instance
celery = make_celery(app)
# celery.conf.update(app.config)


TASK_URL = "http://task-app:8000/task/api/v1/service/"


items = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
    {'id': 3, 'name': 'Item 3'},
]



@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/')
def index():
    consume_kafka_messages.apply_async(args=['test'], countdown=0)
    return jsonify({'status': 'Task scheduled to consume Kafka messages.'}), 202



asgi_handler = WsgiToAsgi(app)

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        import uvicorn
        uvicorn.run(asgi_handler, host='0.0.0.0', port=8000)