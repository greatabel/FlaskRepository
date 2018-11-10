from flask import Flask

app = Flask(__name__)

@app.route('/hi')
@app.route('/hello')
def index():
    return '<h1>Hello Flask!</h1>'