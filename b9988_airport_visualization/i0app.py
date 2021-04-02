import os
import json

from flask import Flask, request
from flask import render_template
from flask import make_response
from flask import jsonify

import csv
from termcolor import colored

def load(filepath):
    rows = []
    with open(filepath,'rt')as f:
      data = csv.reader(f)
      for row in data:
            # print(row, len(row))
            rows.append(row)
    return rows


app = Flask(__name__)
app.debug = True


# mydict = {
#     1: [3, 1.0, 0.391, 0.685],
#     2: [2, 0.0, 0.257, 0.604],
#     3: [2, 0.0, 0.257, 0.604]
# }

@app.route('/home/')
@app.route('/home/<index_id>')
def scp2(index_id=""):
    index = ''
    target = ''
    scores = ''

    query_value = request.args.get('query')

    r = make_response(
        render_template('scp2.html', query_value=query_value,index=index)
        )

    return r

@app.route('/delay/')
def delay():
    r = make_response(
        render_template('airport_delays_congestion.html')
        )

    return r

@app.route('/opensky/')
def opensky():
    r = make_response(
        render_template('opensky.html')
        )

    return r

@app.route('/index/')
def index():
    r = make_response(
        render_template('index.html')
        )

    return r

@app.route('/index_b/')
def index_b():
    r = make_response(
        render_template('index-B.html')
        )

    return r

@app.route("/statistics", methods=['GET'])
def relationship():
    # static/data/test_data.json
    filename = os.path.join(app.static_folder, 'data/data.json')
    with open(filename) as test_file:
        d = json.load(test_file)
    # print(type(d), '#'*10, d)
    return jsonify(d)

if __name__ == '__main__':
    app.run()