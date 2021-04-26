from flask import Flask, url_for, render_template, request, redirect, session, Response
from flask_sqlalchemy import SQLAlchemy


import jellyfish

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

# log相关声明
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)



#  flask 服务相关实例
app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

xs = []
ys = []

# 登录用户相关类
class User(db.Model):
    """ Create user table"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

#  绘图类，暂时可以忽略，没有被使用
@app.route("/plot.png")
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


def create_figure():
    global xs, ys
    fig = Figure()
    axis = fig.add_subplot(2, 1, 1)
    # xs = range(100)
    # ys = [random.randint(1, 50) for x in xs]
    # axis.plot(xs, ys)

    # 二次拟合
    if len(xs) > 0 and len(ys) > 0:
        coef = np.polyfit(xs, ys, 2)
        y_fit = np.polyval(coef, xs)
        axis.plot(xs, y_fit, "g")

    return fig


# @app.route("/", methods=["GET", "POST"])
# def home():
#     global xs, ys
#     """ Session control"""
#     if not session.get("logged_in"):
#         return render_template("index.html")
#     else:
#         if request.method == "POST":
#             mydict = process()

#             mysymptom_dict = process_symptom()
#             print("#" * 20, "mysymptom_dict=", mysymptom_dict)
#             disename = request.form["disename"]
#             symptom = request.form["symptom"]
#             prescrptinfo = request.form["prescrptinfo"]

#             data = None
#             if disename != "":
#                 if disename in mydict:
#                     data = mydict[disename]
#             if symptom != "":
#                 print("symptom=", symptom, "#" * 10)
#                 if symptom in mysymptom_dict:
#                     data = mysymptom_dict[symptom]
#                 else:
#                     for key, value in mysymptom_dict.items():
#                         sname = key
#                         tname = symptom
#                         c0 = jellyfish.levenshtein_distance(sname, tname)
#                         c1 = jellyfish.jaro_distance(sname, tname)
#                         c1 = round(c1, 4)
#                         c2 = jellyfish.damerau_levenshtein_distance(sname, tname)
#                         # https://en.wikipedia.org/wiki/Hamming_distance
#                         c3 = jellyfish.hamming_distance(sname, tname)
#                         print(c0, c1, c2, c3)
#                         # 我们可以更换所有模型，目前使用jaro_distance
#                         if c1 > 0.7:
#                             print("#" * 10, sname, "*" * 10)
#                             data = mysymptom_dict[sname]
#             if prescrptinfo != "":
#                 xs, ys = process_drugday_age(prescrptinfo)
#             return render_template("index.html", data=data)
#         return render_template("index.html")


# 首页的路由操作
@app.route("/", methods=["GET", "POST"])
def home():
    listings = list(range(1, 7))
    # return render_template("home.html", listing=listings)
    print(listings)
    """ Session control"""
    if not session.get("logged_in"):
        return render_template("home.html")
    else:
        if request.method == "POST":
            return render_template("home.html",  listing=listings)
        return render_template("home.html", listing=listings)


# 登录路由
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Form"""
    if request.method == "GET":
        return render_template("home.html")
    else:
        name = request.form["username"]
        passw = request.form["password"]
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session["logged_in"] = True
                return redirect(url_for("home"))
            else:
                return "Not Login"
        except:
            return "Not Login"

# 注册路由
@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register Form"""
    if request.method == "POST":
        new_user = User(
            username=request.form["username"], password=request.form["password"]
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template("home.html")
    return render_template("home.html")


@app.route("/logout")
def logout():
    """Logout Form"""
    session["logged_in"] = False
    return redirect(url_for("home"))


# 推荐页路由
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    import recommandation 
    choosed = recommandation.main()
    print('choosed=', choosed)
    if request.method == "POST":
        print('in post')
        # movie_name = request.form['movie_name']
        # movie_id = request.form['movie_id']
        # rtext = request.form['rtext']
        # rating = request.form['rating']

        # movie = Movie(movie_name, 1990, int(movie_id))
        # review = Review(movie, rtext, int(rating))
        # rc_reviews.append(review)


    return render_template(
        'recommend.html',
        choosed=choosed
        
    )

# 前台播放音乐的位置，名称详细页的维护
def return_dict():
    #Dictionary to store music file information
    dict_here = [
        {'id': 1, 'name': 'Acoustic Breeze', 'link': 'music/acousticbreeze.mp3', 'genre': 'General', 'chill out': 5},
        {'id': 2, 'name': 'Happy Rock','link': 'music/happyrock.mp3', 'genre': 'Bollywood', 'rating': 4},
        {'id': 3, 'name': 'Ukulele', 'link': 'music/ukulele.mp3', 'genre': 'Bollywood', 'rating': 4}
        ]
    return dict_here

#Route to render GUI, 简易播放器的页面
@app.route('/music/<int:music_id>')
def show_entries(music_id):
    print(music_id, '#-#'*20)
    general_Data = {
        'title': 'Music Player'}
    print(return_dict())
    stream_entries = []
    if music_id == 1:
        stream_entries = [{'id': 1, 'name': 'Acoustic Breeze', 'link': 'music/acousticbreeze.mp3', 'genre': 'General', 'chill out': 5}]
    elif music_id == 2:
        stream_entries = [ {'id': 2, 'name': 'Happy Rock','link': 'music/happyrock.mp3', 'genre': 'Bollywood', 'rating': 4}]
    elif music_id == 3:
        stream_entries = [{'id': 3, 'name': 'Ukulele', 'link': 'music/ukulele.mp3', 'genre': 'Bollywood', 'rating': 4}]
    return render_template('simple.html', entries=stream_entries, **general_Data)

#Route to stream music
@app.route('/<int:stream_id>')
def streammp3(stream_id):
    def generate():
        data = return_dict()
        count = 1
        for item in data:
            if item['id'] == stream_id:
                song = item['link']
        with open(song, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
                logging.debug('Music data fragment : ' + str(count))
                count += 1
                
    return Response(generate(), mimetype="audio/mp3")

if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    # app.run(host='0.0.0.0')
    # app.run(host='localhost', port=8000, threaded=False)
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    http_server.debug = True
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
