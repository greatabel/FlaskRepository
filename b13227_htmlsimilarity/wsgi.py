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
# from movie.domain.model import Director, Review, Movie

from html_similarity import style_similarity, structural_similarity, similarity
from common import set_js_file

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
    nickname = db.Column(db.String(80))
    school_class = db.Column(db.String(80))
    school_grade = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    '''
    课程数据模型
    '''
    # 主键ID
    id = db.Column(db.Integer,primary_key = True)
    # 课程标题
    title = db.Column(db.String(100))
    # 课程正文
    text = db.Column(db.Text)
    
    def __init__(self,title,text):
        '''
        初始化方法
        '''
        self.title = title
        self.text = text


# 老师当前布置作业的表
class TeacherWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    detail = db.Column(db.String(500))
    answer = db.Column(db.String(5000))
    course_id = db.Column(db.Integer)

    def __init__(self, title, detail, answer, course_id):
        self.title = title
        self.detail = detail
        self.answer = answer
        self.course_id = course_id

class StudentWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    answer = db.Column(db.String(5000))
    score =  db.Column(db.DECIMAL(10,2))
    course_id = db.Column(db.Integer)

    def __init__(self, userid, answer,score, course_id):
        self.userid = userid
        self.answer = answer
        self.score = score
        self.course_id = course_id

### -------------start of home

class PageResult:
    
    def __init__(self, data, page=1, number=2):
        self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
        self.full_listing = [self.data[i:i+number] for i in range(0, len(self.data), number)]
        self.totalpage = len(data)// number
        print('totalpage=', self.totalpage)


    def __iter__(self):
        if self.page - 1 < len(self.full_listing):
            for i in self.full_listing[self.page-1]:
                yield i
        else:
            return None

    def __repr__(self): #used for page linking
        return "/home/{}".format(self.page+1) #view the next page

@app.route('/home/<int:pagenum>', methods=['GET'])
@app.route('/home', methods=['GET', 'POST'])
def home(pagenum=1):
    print('home '*10)
    blogs = Blog.query.all()
    user = None
    if "userid" in session:
        user = User.query.filter_by(id = session["userid"]).first()
    else:
        print('userid not in session')
    print('in home', user, 'blogs=', len(blogs),'*'*20)
    if request.method == "POST":
        search_list = []
        keyword = request.form['keyword']
        print('keyword=', keyword, '-'*10)
        if keyword is not None:
            for movie in notice_list:
                if movie.director.director_full_name == keyword:
                    search_list.append(movie)

                for actor in movie.actors:
                    if actor.actor_full_name == keyword:
                        search_list.append(movie)
                        break

                for gene in movie.genres:
                    if gene.genre_name == keyword:
                        search_list.append(movie)
                        break
        print('search_list=' ,search_list, '#'*5)
        return rt(
            'home.html',
            listing=PageResult(search_list, pagenum, 2),
            user=user
        )

    return rt(
        'home.html',
        listing=PageResult(blogs, pagenum),
        user=user
        
    )

@app.route('/blogs/create',methods = ['GET', 'POST'])
def create_blog():
    '''
    创建课程文章
    '''
    if request.method == 'GET':
        # 如果是GET请求，则渲染创建页面
        return rt('create_blog.html')
    else:
        # 从表单请求体中获取请求数据
        title = request.form['title']
        text = request.form['text']
        
        # 创建一个课程对象
        blog = Blog(title = title,text = text)
        db.session.add(blog)
        # 必须提交才能生效
        db.session.commit()
        # 创建完成之后重定向到课程列表页面
        return redirect('/blogs')

@app.route('/blogs',methods = ['GET'])
def list_notes():
    '''
    查询课程列表
    '''
    blogs = Blog.query.all()
    # 渲染课程列表页面目标文件，传入blogs参数
    return rt('list_blogs.html',blogs = blogs)


@app.route('/blogs/update/<id>',methods = ['GET', 'POST'])
def update_note(id):
    '''
    更新课程
    '''
    if request.method == 'GET':
        # 根据ID查询课程详情
        blog = Blog.query.filter_by(id = id).first_or_404()
        # 渲染修改笔记页面HTML模板
        return rt('update_blog.html',blog = blog)
    else:
        # 获取请求的课程标题和正文
        title = request.form['title']
        text = request.form['text']
        
        # 更新课程
        blog = Blog.query.filter_by(id = id).update({'title':title,'text':text})
        # 提交才能生效
        db.session.commit()
        # 修改完成之后重定向到课程详情页面
        return redirect('/blogs/{id}'.format(id = id))


@app.route('/blogs/<id>',methods = ['GET','DELETE'])
def query_note(id):
    '''
    查询课程详情、删除课程
    '''
    if request.method == 'GET':
        # 到数据库查询课程详情
        blog = Blog.query.filter_by(id = id).first_or_404()
        print(id, blog, 'in query_blog','@'*20)
        # 渲染课程详情页面
        return rt('query_blog.html',blog = blog)
    else:
        # 删除课程
        blog = Blog.query.filter_by(id = id).delete()
        # 提交才能生效
        db.session.commit()
        # 返回204正常响应，否则页面ajax会报错
        return '',204

### -------------end of home





### -------------start of profile

@app.route('/profile',methods = ['GET','DELETE'])
def query_profile():
    '''
    查询课程详情、删除课程
    '''

    id = session["userid"]

    if request.method == 'GET':

        # 到数据库查询课程详情
        user = User.query.filter_by(id = id).first_or_404()
        print(user.username, user.password, '#'*5)
        # 渲染课程详情页面
        return rt('profile.html',user = user)
    else:
        # 删除课程
        user = User.query.filter_by(id = id).delete()
        # 提交才能生效
        db.session.commit()
        # 返回204正常响应，否则页面ajax会报错
        return '',204



@app.route('/profiles/update/<id>',methods = ['GET', 'POST'])
def update_profile(id):
    '''
    更新课程
    '''
    if request.method == 'GET':
        # 根据ID查询课程详情
        user = User.query.filter_by(id = id).first_or_404()
        # 渲染修改笔记页面HTML模板
        return rt('update_profile.html',user = user)
    else:
        # 获取请求的课程标题和正文
        password = request.form['password']
        nickname = request.form['nickname']
        school_class = request.form['school_class']
        school_grade = request.form['school_grade']
        
        # 更新课程
        user = User.query.filter_by(id = id).update({'password':password,'nickname':nickname,
            'school_class':school_class, 'school_grade':school_grade})
        # 提交才能生效
        db.session.commit()
        # 修改完成之后重定向到课程详情页面
        return redirect('/profile')




### -------------end of profile


@app.route('/course/<id>',methods = ['GET'])
def course_home(id):
    '''
    查询课程详情、删除课程
    '''
    if request.method == 'GET':
        # 到数据库查询课程详情
        blog = Blog.query.filter_by(id = id).first_or_404()
        teacherWork = TeacherWork.query.filter_by(course_id = id).first()
        print(id, blog, 'in query_blog','@'*20)
        # 渲染课程详情页面
        return rt('course.html',blog = blog, teacherWork=teacherWork)
    else:
        return '',204


login_manager = flask_login.LoginManager(app)
user_pass = {}


# @app.route("/call_bash", methods=["GET"])
# def call_bash():
#     i0bash_caller.open_client("")
#     return {}, 200


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

            # w = TeacherWork.query.get(1)
            # print('w=', w, w.answer, w.title)
            # if w is not None:
            #     session['title'] = w.title
            #     session['detail'] = w.detail
            #     session['answer'] = w.answer

            return redirect(url_for("home", pagenum=1))
        else:
            return "Not Login"
    except Exception as e: 
        print(e)
        return "Not Login"
    return redirect(url_for("home", pagenum=1))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for("home", pagenum=1))
    # if DB.get_user(email):
    if email in user_pass:
        print("already existed user")
        return redirect(url_for("home", pagenum=1))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print("register", email, pw1)
    new_user = User(username=email, password=pw1)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("home", pagenum=1))


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("home", pagenum=1))


reviews = []


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":

        movie_name = request.form["movie_name"]
        movie_id = request.form["movie_id"]
        rtext = request.form["rtext"]
        rating = request.form["rating"]
    import glob
    files = glob.glob("upload/*.html")
    files.sort(key=os.path.getmtime)
    # print(files, '#'*30,files[-2],files[-1], '@'*5)

    with open(files[-2], "r") as f:
        html_1 = f.read()
    with open(files[-1], "r") as f:
        html_2 = f.read()
    # print(html_1, '#'*20, html_2)
    myscore = similarity(html_1, html_2)
    mypass = 0
    my_notpass = 0

    num_positive = 0
    num_neural = 0
    num_nagtive = 0
    if 'userid' in session:
        scores  = StudentWork.query.filter_by(userid=session['userid']).all()

        for r in scores:
            if r.score > 0.8:
                mypass += 1
            else:
                my_notpass += 1

            if r.score > 0.8:
                num_positive += 1
            if r.score <= 0.8 and r.score > 0.4:
                num_neural += 1
            if r.score <= 0.4:
                num_nagtive += 1

        print(mypass, my_notpass)
    return rt(
        "review.html",
      
        myscore=round(myscore, 2),
        mypass=mypass,
        my_notpass=my_notpass,
        num_positive=num_positive,
        num_neural=num_neural,
        num_nagtive=num_nagtive
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
    course_id = request.form.get("course_id")
    # print(title,detail, 'course_id=', course_id, '#'*10, 'teacher_work')
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    # print("teacher_work ===>", title, detail)
    w = TeacherWork.query.filter_by(course_id=course_id).first()
    if w is not None:
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
    course_id = request.args.get("course_id")  
    print('course_id in upload= ', course_id, '*'*30)
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
            # w = TeacherWork.query.get(1)
            w = TeacherWork.query.filter_by(course_id=course_id).first()
            print('w=',w)
        # self.title = title
        # self.detail = detail
        # self.answer = answer
        # self.course_id = course_id

            if w is None:
                w = TeacherWork(title='', detail='',answer=html_1, course_id=course_id)
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
            w1 = TeacherWork.query.filter_by(course_id=course_id).first()
            correct_answer = w1.answer
            myscore = similarity(html_2, correct_answer)
            print('#'*20, 'myscore=', myscore)
            set_js_file(myscore)
            s = StudentWork.query.filter_by(course_id=course_id).first()
            print(w1,'s=',s)

            if s is None:
                w = StudentWork(userid=session['userid'],answer=html_2, score=myscore,course_id=course_id)
                db.session.add(w)
                db.session.commit()
            else:
                s.answer = html_2
                s.score = myscore
                db.session.commit()
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
