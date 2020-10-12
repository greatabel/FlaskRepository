from flask import Flask
app = Flask(__name__)


@app.route('/mystudentID/')
def hello():
    return {"studentID": "20085272G"}, 200


@app.route('/airbnb/reviews')
def reviews():
    return {"studentID": "20085272G"}, 200



if __name__ == '__main__':
    app.run()