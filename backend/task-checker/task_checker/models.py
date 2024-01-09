from task_checker.database import db


class Item(db.Model):
    __tablename__ = 'task_details'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)