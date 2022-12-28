import sqlite3
import json
import pandas as pd
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask import abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecret1"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#
# class User(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True)
#     Fname = db.Column(db.String(50), unique=True, nullable=False)
#     Sname = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(50), unique=True, nullable=False)
#
# db.create_all()
#
# marco = User(user_id = 1, Fname = 'Marco', Sname = 'Brescia', email='marcobr@gmail.com',password='thisisatest')
#
# db.session.add(marco)
#
# try:
#     db.session.commit()
# except Exception as e:
#     db.session.rollback()
# finally:
#     db.session.close()
#
# print(User.query.all())
# u = User.query.get(1)
# print(u.email, u.Sname)


politicians = [
    {"id": 1, "Name": "Joe Biden", "Age": 63, "Party": "Democratic"},
    {"id": 2, "Name": "Kamala Harris", "Age": 57, "Party": "Democratic"},
    {"id": 3, "Name": "Mike Pence", "Age": 76, "Party": "Republican"},
    {"id": 4, "Name": "Donald Trump", "Age": 76, "Party": "Republican"},
]

users = {
    "giannyprocida@gmai.com": "football4life",
    "gprocida1690@outlook.com": "Ilovefootball",
}


def get_db_conn():
    dict_cur = sqlite3.connect("usnews.db")
    dict_cur.row_factory = sqlite3.Row
    return dict_cur


@app.route("/")
def Homepage():
    return render_template("Homepage.html", politicians=politicians)


@app.route("/details/<int:id>")
def details(id):
    p = next((p for p in politicians if p["id"] == id), None)
    print(p)
    dict_cur = get_db_conn()
    tableName = p["Name"].split()[1]
    print(tableName)
    if p:
        dict_cur = get_db_conn()
        listofSqliteObj = dict_cur.execute(
            """select * from {0} limit 5""".format(tableName)
        ).fetchall()

        print(listofSqliteObj, listofSqliteObj[0]["Title"])

        ListofDict = [dict(row) for row in listofSqliteObj]

        ListofJsonStr = [json.dumps(dict) for dict in ListofDict]
        print(ListofJsonStr)
        return render_template(
            "details.html",
            politicians=p,
            listofSqliteObj=listofSqliteObj,
            ListofJsonStr=ListofJsonStr,
        )
    else:
        abort(404, description="Error")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        fname = request.form["fname"]
        sname = request.form["sname"]
        email = request.form["email"]
        password = request.form["password"]
        if email in users and users[email] == password:
            return render_template(
                "login.html", message="'You are successfully logged in!'"
            )
        else:
            return render_template("login.html", message="Login failed")
    return render_template("login.html")


@app.route("/About")
def About():
    return render_template("about.html")


@app.route("/survey")
def survey():
    return render_template("survey.html")


if __name__ == "__main__":
    app.run(debug=True)
