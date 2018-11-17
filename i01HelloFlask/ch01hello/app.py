from flask import Flask

app = Flask(__name__)

app.config['ADMIN_NAME'] = 'Peter'

app.config.update(
    TESTING=True,
    SECRET_KEY='123test'
    )


@app.route('/hi')
@app.route('/hello')
def index():
    value = app.config['ADMIN_NAME']
    return '<h1>Hello Flask! ' + value + '</h1>'


@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h>' % name

@app.route('/greet0')
@app.route('/greet0/<name>')
def greet0(name='Programmer'):
    return '<h1>Hello0, %s!</h>' % name