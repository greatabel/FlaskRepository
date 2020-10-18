from flask import Flask, request
from flask import render_template
import sqlite3


app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

typelist = ['参考案例', '法律意见书', '证据目录', '合同文本']



def insert_db(sql, p):

    conn = sqlite3.connect("legaltext.db")
    c = conn.cursor()
    c.execute(sql, p)
    conn.commit()
    conn.close()



@app.route('/add', methods=['GET', 'POST'])
def add():
    errors = []
    result = {}
    if request.method == "POST":
        # get url that the user has entered
        p = None
        sql = None

        select_Items = request.form['select_Items']
        title = request.form['title']
        content = request.form['content']

        if select_Items == 'tb1':
            case_court = request.form['case_court']
            case_year = request.form['case_year']
            case_id = request.form['case_id']
            case_cause = request.form['case_cause']
            case_industry = request.form['case_industry']
            p = (title, content, case_court, case_year, case_id, case_cause, case_industry)
            sql = "INSERT INTO reference (title, content, case_court, case_year, case_id, case_cause, case_industry)\
                    VALUES (?, ?, ?, ?, ?, ?, ?)"

        elif select_Items == 'tb2':
            ''
        elif select_Items == 'tb3':
            ''
        elif select_Items == 'tb4':
            ''
        insert_db(sql, p)
        # try:
        #     url = request.form['url']
        #     r = requests.get(url)
        #     print(r.text)
        # except:
        #     errors.append(
        #         "Unable to get URL. Please make sure it's valid and try again."
        #     )
    return render_template('add.html', typelist=typelist,
                 errors=errors, result=result)


if __name__ == '__main__':
    app.run()