from flask import Blueprint, jsonify

from task_checker.tasks_flask import consume_kafka_messages
from task_checker.models import Item


router = Blueprint('router', __name__)

TASK_URL = "http://task-app:8000/task/api/v1/service/"

@router.route('/')
def index():
    consume_kafka_messages.apply_async(args=['test'], countdown=0, queue="queue_for_task2")
    return jsonify({'status': 'Task scheduled to consume Kafka messages.'}), 202

@router.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'title': item.title, 'description': item.description} for item in items])
    # return "hello"