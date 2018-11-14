from flask import Flask

app = Flask(__name__)

@app.route('/hi')
@app.route('/hello')
def index():
    return '<h1>Hello Flask!</h1>'

@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h>' % name