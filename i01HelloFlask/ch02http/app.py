from flask import Flask, request

app = Flask(__name__)



@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    return '<h1>Hello: ' + name + '</h1>'

