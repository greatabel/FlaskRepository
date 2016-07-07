from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    print('#',email,password)

    if  email  and  password and (email == "abel") :
        return redirect(url_for('measure'))
    return home()

@app.route("/logout")
def logout():
    # logout_user()
    print('logout')
    return redirect(url_for("home"))


@app.route("/measure")
def measure():
    return render_template("measure.html")

@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)