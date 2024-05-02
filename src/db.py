from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.password = kwargs.get("password", "")

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
        }

    def serialize(self):
        tasks = [t.serialize() for t in self.tasks]
        tasks = sorted(tasks, key=lambda task: (-task["priority"], task["deadline"]))

        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "tasks": [t.serialize() for t in self.tasks],
        }


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    time_to_complete = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.deadline = kwargs.get("deadline")
        self.priority = kwargs.get("priority", 1)
        self.time_to_complete = kwargs.get("time_to_complete", "")
        self.done = kwargs.get("done", False)
        self.user_id = kwargs.get("user_id")

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "deadline": self.deadline.isoformat(),
            "priority": self.priority,
            "time_to_complete": self.time_to_complete,
            "done": self.done,
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "deadline": self.deadline.isoformat(),
            "priority": self.priority,
            "time_to_complete": self.time_to_complete,
            "done": self.done,
            "user_id": self.user_id,
        }
