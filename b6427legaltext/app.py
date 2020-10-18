from flask import Flask, request
from flask import render_template


app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

typelist = ['法律意见书','参考案例', '合同文本', '证据目录']


@app.route('/add')
def add():
    # input :http://www.baidu.com
    query_value = request.args.get('query')
    index =  " is here"
    return render_template('add.html', typelist=typelist,index=index)


if __name__ == '__main__':
    app.run()