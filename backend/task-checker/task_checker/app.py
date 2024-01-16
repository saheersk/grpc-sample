from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from task_checker.routers.new_task import router
from task_checker.celery_instance import celery
from task_checker.database import db


app = Flask(__name__)


app.config['SECRET_KEY'] = '982374989364876jasdfhskjd'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://checker_user:checker_user123@postgres-flask-service:5432/checker_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://checker_user:checker_user123@postgres_checker:5432/checker_db'
CORS(app, origins=["http://task-auth:8000", "http://localhost:8001"])

def make_celery(app):
    celery.conf.update(app.config)
    return celery

make_celery(app)

db.init_app(app)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '982374989364876jasdfhskjd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://checker_user:checker_user123@postgres_checker:5432/checker_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    make_celery(app)

    Migrate(app, db)

    app.register_blueprint(router, url_prefix='/flask')

    return app



