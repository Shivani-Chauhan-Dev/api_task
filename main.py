from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import uuid


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///create_task.db"
db = SQLAlchemy()
db.init_app(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(500))
    comments=db.Column(db.String(50))
    status=db.Column(db.String(10))
    created=db.Column(db.String(20))
    lastupdated=db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'comments':self.comments,
            'status': self.status,
            'created': self.created,
            'lastupdated': self.lastupdated
        }

with app.app_context():
    db.create_all()




@app.route("/task",methods=["Post"])
def creat_task():
    current_date=str(datetime.datetime.now())
    a = json.loads(request.data)
    name =a.get("name")
    comments=a.get("comments")
    status=a.get("status")
    id=uuid.uuid1().int>>64
    created=current_date
    lastupdate=current_date

    entry=Task(name=name,comments=comments,status=status,id=id,created=created,lastupdated=lastupdate)
    db.session.add(entry)
    db.session.commit()


    return jsonify(entry.to_dict())


@app.route("/task",methods=["Get"])
def get_task():
    task= Task.query.all()
    print(task)
    task_list = []
    for get_task in task:
        # print(get_task)
        task_list.append({"id":get_task.id,"name":get_task.name,"comments":get_task.comments,"status":get_task.status,"created":get_task.created,"lastupdate":get_task.lastupdated})


    return jsonify(task_list)


@app.route("/task/<int:task_id>",methods=["Get"])
def find_task(task_id):
    task=Task.query.get(task_id)

    task_data=({"id":task.id,"name":task.name,"comments":task.comments,"status":task.status,"created":task.created,"lastupdate":task.lastupdated})

    return jsonify(task_data)


@app.route("/task/<int:task_id>",methods=["Put"])
def update_task(task_id):
    # current_date=str(datetime.datetime.now())
    task=Task.query.get(task_id)
    a=(json.loads(request.data))
    name =a.get("name")
    comments=a.get("comments")
    status =a.get("status")

    task.name =name
    task.comments=comments
    task.status=status


    db.session.commit()
    new_data=({"id":task.id,"name":task.name,"comments":task.comments,"status":task.status,"created":task.created,"lastupdate":task.lastupdated})

    return jsonify(new_data)

@app.route("/task/<int:task_id>",methods=["Delete"])
def delete_task(task_id):
    task=Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify("delete successfully")












































if __name__ =="__main__":
    app.run(debug=True)
