from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
# 连接数据库，这里要注意的就是ajax数据库要提前在数据库中建立好
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost:3306/ajax"
# 自动提交功能
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
db = SQLAlchemy(app)


# 创建一个实体类，对应者一张表
class Users(db.Model):
    # 表名为
    __tablename__ = "users"
    # 建立字段
    uid = db.Column(db.Integer, primary_key=True)
    uloginname = db.Column(db.String(30))
    uloginpwd = db.Column(db.String(30))
    uname = db.Column(db.String(30))

    # 初始化
    def __init__(self, uloginname, uloginpwd, uname):
        self.uloginname = uloginname
        self.uloginpwd = uloginpwd
        self.uname = uname

    # 打印数据格式为
    def __repr__(self):
        return "<Users:%r>" % self.uname

# 这里才是真正的创建表了
db.create_all()


# 首页
@app.route('/')
def hello_world():
    return '注册成功'


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("01-login.html")
    else:
        # 点击注册之后，将所有的数据存储到数据库中，并且重定向到首页
        loginname = request.form.get("loginname")
        loginpwd = request.form.get("loginpwd")
        uname = request.form.get("uname")
        user = Users(loginname, loginpwd, uname)
        db.session.add(user)
        return redirect("/")


@app.route('/01-server')
def server():
    # 接收前端传递过来的参数 - lname,这里是接收ajax传过来是数据
    lname = request.args.get("lname")
    # 以lanme作为条件，通过Users实体类查询数据
    user = Users.query.filter_by(uloginname=lname).first()
    # 如果查询出来了数据的话则说明登录名称已存在，否则通过
    if user:
        return "用户名称已存在"
    else:
        return "通过"


if __name__ == '__main__':
    app.run(debug=True)
