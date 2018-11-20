from flask import Flask, request

app = Flask(__name__)



@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    return '<h1>Hello: ' + name + '</h1>'

@app.route('/hello0', methods=['GET', 'POST'])
def hello0():
    return '<h1>Hello, Flask</h1>'