import json
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost:3306/ajax"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    uloginname = db.Column(db.String(30))
    uloginpwd = db.Column(db.String(30))
    uname = db.Column(db.String(30))

    def to_dict(self):
        dic = {
            "id" : self.uid,
            "loginname" : self.uloginname,
            "loginpwd" : self.uloginpwd,
            "username" : self.uname
        }
        return dic


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/01-allusers")
def allusers():
    return render_template("01-allusers.html")


@app.route('/01-server')
def server01():
    users = Users.query.all()
    info_list = list()
    for user in users:
        info_dict = {}
        name = user.uloginname
        age = user.uloginpwd
        uname = user.uname
        info_dict["name"] = name
        info_dict["age"] = age
        info_dict["uname"] = uname
        info_list.append(info_dict)
    return json.dumps(info_list)


@app.route('/02-json')
def json_views():
    list = ["fan bing bing", "范冰冰", "Li Chen"]
    jsonstr = json.dumps(list)
    return jsonstr


@app.route('/02-html')
def html_views():
    return render_template("02-json.html")


@app.route('/03-users')
def users():
    return render_template("03-users.html")


@app.route('/03-server')
def server03():
    # 读取users表中id=1的用户信息
    # user = Users.query.filter_by(uid=1).first()
    user = Users.query.all()
    list = []
    for x in user:
        list.append(x.to_dict())
    return json.dumps(list)


@app.route('/04-show')
def html04_views():
    return render_template("04-show.html")


@app.route('/04-server')
def server04():
    user = Users.query.all()
    list = []
    for x in user:
        list.append(x.to_dict())
    return json.dumps(list)


@app.route('/04-delete')
def delete():
    # 先获取前端传递过来的id值
    id = request.args.get("id")
    user = Users.query.filter_by(uid=id).first()
    try:
        db.session.delete(user)
        dic = {
            "status": 1,
            "msg": "删除成功"
        }
    except Exception as e:
        print(e)
        dic = {
            "status": 0,
            "msg": "删除失败，请联系管理员"
        }
    return json.dumps(dic)


if __name__ == '__main__':
    app.run(debug=True)
