import json
from flask import Flask, request
import dao
from db import db
from db import Task, User
from sqlalchemy import desc

app = Flask(__name__)
db_filename = "todo.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


# task routes


# Get all tasks from a user, sorted by priority (1-5 where 5 is highest). If tasks have the
# same priority, they are sorted by the soonest deadline.
@app.route("/tasks/<int:user_id>/")
def get_all_tasks(user_id):
    tasks = Task.query.order_by(desc(Task.priority), Task.deadline).all()


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")
    return success_response(task.serialize())


# Create a task taking in the Name, Priority (1-5), Deadline, Time to complete, Completed
@app.route("/tasks/<int:user_id>", methods=["POST"])
def create_task(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")

    body = json.loads(request.data)
    new_task = Task(
        name=body.get("name"),
        deadline=body.get("deadline"),
        priority=body.get("priority"),
        time_to_complete=body.get("time_to_complete"),
        done=body.get("done", False),
    )
    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
