"""App entry point."""
import os
import sys
import json

import flask_login
from flask import request
from flask import url_for
from flask import redirect, session
from flask import Blueprint, render_template as rt
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, Response
from flask import jsonify

from movie import create_app
from movie.domain.model import Director, Review, Movie

from html_similarity import style_similarity, structural_similarity, similarity
# from common import set_js_file

app = create_app()
app.secret_key = "ABCabc123"
app.debug = True

# ---start  数据库 ---

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hs_data.db"
db = SQLAlchemy(app)

# --- end   数据库 ---
admin_list = ['admin@126.com']

class User(db.Model):
    """ Create user table"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# 老师当前布置作业的表
class TeacherWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    detail = db.Column(db.String(500))
    answer = db.Column(db.String(5000))

    def __init__(self, title, detail, answer):
        self.title = title
        self.detail = detail
        self.answer = answer


class StudentWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    answer = db.Column(db.String(5000))
    score =  db.Column(db.DECIMAL(10,2))

    def __init__(self, title, detail, answer):
        self.userid = title
        self.answer = detail
        self.score = answer


login_manager = flask_login.LoginManager(app)
user_pass = {}


@app.route("/call_bash", methods=["GET"])
def call_bash():
    i0bash_caller.open_client("")
    return {}, 200


@app.route("/statistics", methods=["GET"])
def relationship():
    # static/data/test_data.json
    filename = os.path.join(app.static_folder, "data.json")
    with open(filename) as test_file:
        d = json.load(test_file)
    print(type(d), "#" * 10, d)
    return d


@login_manager.user_loader
def load_user(email):
    print('$'*30)
    return user_pass.get(email, None)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        data = User.query.filter_by(username=email, password=password).first()
        print(data, "@" * 10)
        if data is not None:
            print("test login")
            session["logged_in"] = True



            if email in admin_list:
                session["isadmin"] = True
                session["userid"] = data.id

            print("login sucess", "#" * 20, session["logged_in"])

            w = TeacherWork.query.get(1)
            print('w=', w, w.answer, w.title)
            if w is not None:
                session['title'] = w.title
                session['detail'] = w.detail
                session['answer'] = w.answer

            return redirect(url_for("home_bp.home", pagenum=1))
        else:
            return "Not Login"
    except:
        return "Not Login"
    return redirect(url_for("home_bp.home", pagenum=1))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for("home_bp.home", pagenum=1))
    # if DB.get_user(email):
    if email in user_pass:
        print("already existed user")
        return redirect(url_for("home_bp.home", pagenum=1))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print("register", email, pw1)
    new_user = User(username=email, password=pw1)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("home_bp.home", pagenum=1))


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("home_bp.home", pagenum=1))


reviews = []


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":

        movie_name = request.form["movie_name"]
        movie_id = request.form["movie_id"]
        rtext = request.form["rtext"]
        rating = request.form["rating"]

        movie = Movie(movie_name, 1990, int(movie_id))
        review = Review(movie, rtext, int(rating))
        reviews.append(review)

    with open(r'upload/a.html', "r") as f:
        html_1 = f.read()
    with open(r'upload/b.html', "r") as f:
        html_2 = f.read()
    print(html_1, '#'*20, html_2)
    myscore = similarity(html_1, html_2)
    return rt(
        "review.html",
        reviews=reviews,
        myscore=myscore
    )


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized"


# --------------------------
@app.route("/assignwork", methods=["GET"])
def assignwork():
    return rt("index.html")


@app.route("/teacher_work", methods=["POST"])
def teacher_work():
    title = request.form.get("title")
    detail = request.form.get("detail")

    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print("teacher_work ===>", title, detail)
    w = TeacherWork.query.get(1)
    print(w.id, w.answer)
    w.title = title
    w.detail = detail
    db.session.commit()
    session['title'] = title
    session['detail'] = detail

    return redirect(url_for("assignwork"))


@app.route("/student_work", methods=["POST"])
def student_work():
    return redirect(url_for("student_index"))


@app.route("/student_index", methods=["GET"])
def student_index():
    return rt("student_index.html")
# @app.route("/", methods=["GET"])
# def index():
#     return rt("index.html")


@app.route("/file/upload", methods=["POST"])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get("task_id")  # 获取文件的唯一标识符
    chunk = request.form.get("chunk", 0)  # 获取该分片在所有分片中的序号
    filename = "%s%s" % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files["file"]
    upload_file.save("./upload/%s" % filename)  # 保存分片到本地
    return rt("index.html")


@app.route("/file/merge", methods=["GET"])
def upload_success():  # 按序读出分片内容，并写入新文件
    target_filename = request.args.get("filename")  # 获取上传文件的文件名
    task = request.args.get("task_id")  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open("./upload/%s" % target_filename, "wb") as target_file:  # 创建新文件
        while True:
            try:
                filename = "./upload/%s%d" % (task, chunk)
                source_file = open(filename, "rb")  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    if 'isadmin' in session and session['isadmin']:
        print('admin upload assignwork=', target_filename)
        with open(r'upload/'+target_filename, "r") as f:
            html_1 = f.read()
            w = TeacherWork.query.get(1)
            print('w=',w)

            if w is None:
                w = TeacherWork(title='', detail='',answer=html_1)
                db.session.add(w)
                db.session.commit()
            else:
                w.answer = html_1
                db.session.commit()
    else:
        # student submit
        with open(r'upload/'+target_filename, "r") as f:
            html_2 = f.read()
            # print(html_2, '*'*20, session['answer'])
            myscore = similarity(html_2, session['answer'])
            print('#'*20, 'myscore=', myscore)
            # set_js_file(myscore)
    return rt("index.html")


@app.route("/file/list", methods=["GET"])
def file_list():
    files = os.listdir("./upload/")  # 获取文件目录
    # print(type(files))
    files.remove(".DS_Store")
    # files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
    return rt("list.html", files=files)


@app.route("/file/download/<filename>", methods=["GET"])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = "./upload/%s" % filename
        with open(store_path, "rb") as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type="application/octet-stream")


# --------------------------





if __name__ == "__main__":
    db.create_all()

    app.run(host="localhost", port=5000, threaded=False)
