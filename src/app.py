import json
from flask import Flask, request
from db import db
from db import Task, User
from sqlalchemy import desc
from datetime import datetime

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
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps(message), code


# user routes


# Get all current users
@app.route("/users/")
def get_all_users():
    users = [u.serialize() for u in User.query.all()]
    return success_response(users)


# Get user based on user_id
@app.route("/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Course not found!")
    return success_response(user.serialize())


# Create a user
@app.route("/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    new_user = User(name=body.get("name"), password=body.get("password"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/users/<int:user_id>/", methods=["POST"])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    user.name = body.get("name", user.name)
    user.password = body.get("password", user.password)

    db.session.commit()
    return success_response(user.serialize())


@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


# task routes


# Create a task taking in the Name, Priority (1-5), Deadline, Time to complete, Completed
@app.route("/tasks/users/<int:user_id>/", methods=["POST"])
def create_task(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")

    body = json.loads(request.data)

    new_task = Task(
        name=body.get("name"),
        deadline=datetime.fromtimestamp(body.get("deadline")),
        priority=body.get("priority"),
        time_to_complete=body.get("time_to_complete"),
        done=body.get("done", False),
        user_id=user_id,
    )
    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize(), 201)


# Get all tasks from a user, sorted by priority (1-5 where 5 is highest). If tasks have the
# same priority, they are sorted by the soonest deadline.
@app.route("/tasks/users/<int:user_id>/")
def get_user_tasks(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    tasks = [task.serialize() for task in user.tasks]
    return success_response(tasks)


## Get a task from a specific task_id
@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")
    return success_response(task.serialize())


# Updates a task depending on the fields that the user chooses to update
@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")

    body = json.loads(request.data)
    task.name = body.get("name", task.name)
    task.deadline = body.get("deadline", task.deadline)
    task.priority = body.get("priority", task.priority)
    task.time_to_complete = body.get("time_to_complete", task.time_to_complete)

    db.session.commit()
    return success_response(task.serialize())


# Delete a task based on its id
@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found!")

    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
