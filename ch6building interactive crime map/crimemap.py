from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request

from flask_restful import Api

from flask_restful import Resource, reqparse
import json


app = Flask(__name__)
DB = DBHelper()

api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('deviceid')
parser.add_argument('data')

class UserApi(Resource):
        def get(self, userid=None):
            data = DB.get_measure()
            print('abel::',data)
            res = {}
            for m in data:
                res[m[0]] = {
                    'rawdataid': m[1],
                    'data': m[2],
                    'deviceid': m[3],
                    'createdate': str(m[4])
                }
            myresult = json.dumps(res)
            print('abel##:',myresult)
            return myresult

        def post(self, userid):
           # Create a new product
            args = parser.parse_args()
            print(args['deviceid'],'@@',args['data'],'#',args)
            DB.add_measure(args)
            return 'This is a POST response'

        def put(self, userid):
           # Update the product with given id
            return 'This is a PUT response'

        def delete(self, userid):
           # Delete the product with given id
            return 'This is a DELETE response'


api.add_resource(
    UserApi,
    '/api/user',
    '/api/user/<int:userid>/measures',

)

@app.route("/")
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        print('data=',data)
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()

if __name__ == '__main__':
    app.run(port=50001, debug=True)
