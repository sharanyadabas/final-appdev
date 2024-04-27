from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association_table = db.Table(
#     "association",
#     db.Model.metadata,
#     db.Column("task_id",db.Integer,db.ForeignKey("tasks.id")),
#     db.Column("category_id",db.Integer, db.ForeignKey("categories.id"))
# )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)

    def __init__(self,**kwargs):
        self.name = kwargs.get("name","")
        self.password = kwargs.get("password","")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password
        }


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    deadline = db.Column(db.String,nullable=False)
    priority = db.Column(db.Integer,nullable=False)
    time_to_complete = db.Column(db.String,nullable=False)
    done = db.Column(db.Boolean,nullable=False)

    def __init__(self,**kwargs):
        self.name = kwargs.get("description","")
        self.deadline = kwargs.get("deadline","") 
        self.priority = kwargs.get("priority",0)
        self.time_to_complete = kwargs.get("time_to_complete","")       
        self.done = kwargs.get("done",False)

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "deadline": self.deadline,
            "priority": self.priority,
            "time_to_complete": self.time_to_complete,
            "done":self.done
        }