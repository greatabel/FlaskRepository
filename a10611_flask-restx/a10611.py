import os
import json

from flask import Flask, request
from flask_restx import Resource, Api

from flask import jsonify







app = Flask(__name__)
app.debug = True


api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


if __name__ == '__main__':
    app.run(debug=True)