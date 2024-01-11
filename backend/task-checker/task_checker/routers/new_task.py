# import asyncio
from flask import Blueprint, jsonify

from task_checker.tasks_flask import consume_kafka_messages, async_subscribe
from task_checker.models import Item


router = Blueprint('router', __name__)

TASK_URL = "http://task-app:8000/task/api/v1/service/"

@router.route('/', methods=['GET'])
def index():
    consume_kafka_messages.apply_async(args=['test'], countdown=0, queue="queue_for_task2")
    return jsonify({'status': 'Task scheduled to consume Kafka messages.'}), 202


@router.route('/nat', methods=['GET'])
def nat_process():
    # asyncio.run(subscribe("my_subject"))
    async_subscribe.delay(subject="my_subject")
    return jsonify({'status': 'Task scheduled nats to consume Kafka messages.'}), 202


@router.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'title': item.title, 'description': item.description} for item in items])