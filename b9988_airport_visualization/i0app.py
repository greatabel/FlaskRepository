from flask import Flask, request
from flask import render_template
from flask import make_response

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

# 目标id， 目标name相似度， 目标bio相似度，目标头像相似度
mydict = {
    1: [3, 1.0, 0.391, 0.685],
    2: [2, 0.0, 0.257, 0.604],
    3: [2, 0.0, 0.257, 0.604]
}

@app.route('/find_connect/')
@app.route('/find_connect/<index_id>')
def scp2(index_id=""):
    index = ''
    target = ''
    scores = ''

    query_value = request.args.get('query')

    r = make_response(
        render_template('scp2.html', query_value=query_value,index=index)
        )

    return r





if __name__ == '__main__':
    app.run()