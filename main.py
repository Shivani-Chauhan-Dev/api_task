from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import uuid
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///create_task.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://task_pzpf_user:FgAaTjk3UORkTD0BHhiYTcSXJB7QyPy3@dpg-cubij5a3esus73etfi1g-a.oregon-postgres.render.com/task_pzpf"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy()
db.init_app(app)

class Task(db.Model):
    id = db.Column(db.BigInteger,primary_key=True)
    name = db.Column(db.String(60))
    comments=db.Column(db.String(100))
    status=db.Column(db.String(80))
    created=db.Column(db.String(80))
    lastupdated=db.Column(db.String(80))

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'comments':self.comments,
    #         'status': self.status,
    #         'created': self.created,
    #         'lastupdated': self.lastupdated
    #     }

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
    # print(task)
    task_list = []
    for get_task in task:
        # print(get_task)
        task_list.append({"id":get_task.id,"name":get_task.name,"comments":get_task.comments,"status":get_task.status,"created":get_task.created,"lastupdate":get_task.lastupdated})


    return jsonify(task_list)
    # return jsonify(task.to_dict())


@app.route("/task/<int:task_id>",methods=["Get"])
def find_task(task_id):
    task=Task.query.get(task_id)

    task_data=({"id":task.id,"name":task.name,"comments":task.comments,"status":task.status,"created":task.created,"lastupdate":task.lastupdated})
    print(task_data)

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
    app.run(debug=True,port=5002)
