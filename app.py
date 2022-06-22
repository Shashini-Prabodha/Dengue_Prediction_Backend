import json

from flask import Flask, request, redirect, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os
import enum


app = Flask(__name__)
app.secret_key = "super secret key"

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    task = db.relationship("Task", backref="user", lazy=True)


class TaskStatus(enum.Enum):
    DONE = "Done"
    PENDING = "Pending"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    date = db.Column(db.String(250), nullable=False)


db.create_all()


@app.route('/login', methods=["POST", "GET"])
def login():
    # if request.method == "POST":
    #     username = request.form["username"]
    #
    #     existing_user = User.query.filter_by(username=username).first()
    #     print(existing_user)
    #     if existing_user is None:
    #         user = User(username=username)
    #         db.session.add(user)
    #         db.session.commit()
    #         existing_user = user
    #
    #     session["user_id"] = existing_user.id
    #     return redirect("/task")
    # return render_template("login.html")

    articles = User.query.all()
    print(type(articles))

    # return Response(json.dumps(articles),  mimetype='application/json')
    return jsonify(results=articles)

if __name__ == '__main__':
    app.run(debug=True)
