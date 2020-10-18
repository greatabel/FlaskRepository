from flask import Flask, request
from flask import render_template


app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

typelist = ['参考案例', '法律意见书', '证据目录', '合同文本']


@app.route('/add')
def add():
    errors = []
    result = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('add.html', typelist=typelist,
        result=result)


if __name__ == '__main__':
    app.run()