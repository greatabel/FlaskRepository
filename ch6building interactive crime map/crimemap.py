from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request

from flask_restful import Api

from flask_restful import Resource, reqparse, abort
import json


app = Flask(__name__)
DB = DBHelper()

api = Api(app)

Userids = {
    0,
    1,
    2
}

def abort_if_todo_doesnt_exist(userid):
    if userid not in Userids:
        abort(404, message="user's data {} doesn't exist".format(userid))

parser = reqparse.RequestParser()
parser.add_argument('rawdata')
parser.add_argument('whicheye')

class UserApi(Resource):
        def get(self, userid=None):
            print('userid=', userid)
            data = DB.get_rawmeasure(str(userid))
            print('abel::',data)
            res = []
            for m in data:
                d = {}
                d[m[0]] = {
                    'rawdata': m[1],
                    'patientid': m[2],
                    'whicheye': str(m[3]),
                    'createdate': str(m[4])
                }
                res.append(d)
            myresult = json.dumps(res)
            print('abel##:',myresult)
            return myresult

        def post(self, userid):
           # Create a new product
            args = parser.parse_args()
            print('#',args)
            print(args['rawdata'],'@@',args['whicheye'],'#',args)
            DB.add_rawmeasure(args)
            abort_if_todo_doesnt_exist(userid)
            return 201

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
    app.run(port=5000, debug=True)
