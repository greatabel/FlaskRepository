from flask import Flask, request
from flask import render_template
import sqlite3


app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

typelist = ['参考案例', '法律意见书', '证据目录', '合同文本']



def insert_db(sql, p):
    print('#'*5, p, len(p))
    print('@'*5, sql)
    conn = sqlite3.connect("legaltext.db")
    c = conn.cursor()
    c.execute(sql, p)
    conn.commit()
    conn.close()


def select_db(sql):
    print('-^-'*5, sql)
    viewdata = []
    with sqlite3.connect("legaltext.db") as db:
        cursor = db.cursor()    
        cursor.execute(sql)
        viewdata = cursor.fetchall()
    db.commit()
    return viewdata


@app.route('/add', methods=['GET', 'POST'])
def add():
    errors = []
    result = None
    if request.method == "POST":
        # get url that the user has entered
        p = None
        sql = None

        select_Items = request.form['select_Items']


        if select_Items == 'tb1':
            title = request.form['title1']
            content = request.form['content1']
            content = content.strip()
            case_court = request.form['case_court']
            case_year = request.form['case_year']
            case_id = request.form['case_id']
            case_cause = request.form['case_cause']
            case_industry = request.form['case_industry']
            select_sql = "select title from reference where title='" + title + "'"
            p = (title, content, case_court, case_year, case_id, case_cause, case_industry)
            sql = "INSERT INTO reference (title, content, case_court, case_year, case_id, case_cause, case_industry)\
                    VALUES (?, ?, ?, ?, ?, ?, ?)"
        elif select_Items == 'tb2':
            title = request.form['title2']
            content = request.form['content2']
            content = content.strip()
            memo_issue = request.form['memo_issue']
            memo_year = request.form['memo_year']
            meomo_industry = request.form['meomo_industry']
            memo_caseid = request.form['memo_caseid']
            select_sql = "select title from memo where title='" + title + "'"
            p = (title, content, memo_issue, memo_year, meomo_industry, memo_caseid)
            sql = "INSERT INTO memo (title, content, memo_issue, memo_year, meomo_industry, memo_caseid)\
                    VALUES (?, ?, ?, ?, ?, ?)"
        elif select_Items == 'tb3':
            title = request.form['title3']
            content = request.form['content3']
            content = content.strip()
            evidence_cause = request.form['evidence_cause']
            evidence_plaintiff = request.form['evidence_plaintiff']
            evidence_nation = request.form['evidence_nation']
            evidence_industry = request.form['evidence_industry']
            evidence_court = request.form['evidence_court']
            select_sql = "select title from evidence where title='" + title + "'"
            p = (title, content, evidence_cause, evidence_plaintiff, evidence_nation, evidence_industry, evidence_court)
            sql = "INSERT INTO evidence (title, content, evidence_cause, evidence_plaintiff, evidence_nation, evidence_industry, evidence_court)\
                    VALUES(?, ?, ?, ?, ?, ?, ?)"



        elif select_Items == 'tb4':
            title = request.form['title4']
            content = request.form['content4']
            content = content.strip()
            contract_type = request.form['contract_type']
            contract_language = request.form['contract_language']
            contract_amount = request.form['contract_amount']
            contract_position = request.form['contract_position']
            contract_industry = request.form['contract_industry']
            select_sql = "select title from contract where title='" + title + "'"            
            p = (title, content, contract_type, contract_language, contract_amount, contract_position, contract_industry)
            sql = "INSERT INTO contract (title, content, contract_type, contract_language, contract_amount, contract_position, contract_industry)\
                    VALUES(?, ?, ?, ?, ?, ?, ?)"

        r = select_db(select_sql)
        # 不存在这个title
        if len(r) == 0:
            insert_db(sql, p)
            result = '数据插入成功'
        else:
            errors.append('已经存在该标题数据在数据库中')
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


@app.route('/search', methods=['GET', 'POST'])
def search():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        select_Items = request.form['select_Items']   
        p = None
        sql = None
        if select_Items == 'tb1':
            case_court = request.form['case_court'] 
            case_year = request.form['case_year']
            case_id = request.form['case_id']
            case_cause = request.form['case_cause']
            case_industry = request.form['case_industry']
            sql =  """select title, content,
                 (case_court || " " || case_year 
                    || " " || case_id|| " " || case_cause
                    || " " || case_industry) AS tag from reference where """
            if case_court:
                sql += """ case_court='""" + case_court + """' """
            if case_year:
                if case_court != '':
                    sql += """ and """
                sql += """  case_year='""" + case_year + """' """
            if case_id:
                if case_year  != '':
                    sql += """ and """
                sql += """  case_id='""" + case_id  + """' """
            if case_cause:
                if case_id  != '':
                    sql += """ and """

                sql += """  case_cause='""" + case_cause + """' """
            if case_industry:
                if case_cause  != '':
                    sql += """ and """               
                sql += """  case_id='""" + case_industry  + """' """


        elif select_Items == 'tb2':
            memo_issue = request.form['memo_issue']
            memo_year = request.form['memo_year']
            meomo_industry = request.form['meomo_industry']
            memo_caseid = request.form['memo_caseid']
            sql =  """select title, content ,
                 (memo_issue || " " || memo_year 
                    || " " || meomo_industry|| " " || memo_caseid
                    ) AS tag from memo where """
            if memo_issue:
                sql += """ memo_issue='""" + memo_issue + """' """
            if memo_year:
                if memo_issue  != '':
                    sql += """ and """                
                sql += """ memo_year='""" + memo_year + """' """
            if meomo_industry:
                if memo_year  != '':
                    sql += """ and """                  
                sql += """  meomo_industry='""" + meomo_industry  + """' """
            if memo_caseid:
                if meomo_industry  != '':
                    sql += """ and """                  
                sql += """  memo_caseid='""" + memo_caseid  + """' """
        elif select_Items == 'tb3':
            evidence_cause = request.form['evidence_cause']
            evidence_plaintiff = request.form['evidence_plaintiff']
            evidence_nation = request.form['evidence_nation']
            evidence_industry = request.form['evidence_industry']
            evidence_court = request.form['evidence_court']
            sql =  """select title, content,
                 (evidence_cause || " " ||  (CASE evidence_plaintiff WHEN true THEN '原告' ELSE '非原告' END)
                    || " " || evidence_nation|| " " || evidence_industry
                    || " " || evidence_court) AS tag from evidence where """
            if evidence_cause:
                sql += """ evidence_cause='""" + evidence_cause + """' """
            if evidence_plaintiff:
                if evidence_cause  != '':
                    sql += """ and """                           
                sql += """ evidence_plaintiff='""" + evidence_plaintiff + """' """
            if evidence_nation:
                if evidence_plaintiff  != '':
                    sql += """ and """                                          
                sql += """  evidence_nation='""" + evidence_nation + """' """
            if evidence_industry:
                if evidence_nation  != '':
                    sql += """ and """                 
                sql += """  evidence_industry='""" + evidence_industry + """' """
            if evidence_court:
                if evidence_industry  != '':
                    sql += """ and """                 
                sql += """  evidence_court='""" + evidence_court + """' """

        elif select_Items == 'tb4':
            contract_type = request.form['contract_type']
            contract_language = request.form['contract_language']
            contract_amount = request.form['contract_amount']
            contract_position = request.form['contract_position']
            contract_industry = request.form['contract_industry']
            sql =  """select title, content,
                 (contract_type || " " || contract_language 
                    || " " || contract_amount|| " " || contract_position
                    || " " || contract_industry) AS tag from contract where """
            if contract_type:
                sql += """ contract_type='""" + contract_type + """' """
            if contract_language:
                if contract_type  != '':
                    sql += """ and """                                    
                sql += """ contract_language='""" + contract_language + """' """
            if contract_amount:
                if contract_language  != '':
                    sql += """ and """                   
                sql += """  contract_amount='""" + contract_amount  + """' """
            if contract_position:
                if contract_amount  != '':
                    sql += """ and """                  
                sql += """  contract_position='""" + contract_position + """' """
            if contract_industry:
                if contract_position  != '':
                    sql += """ and """                 
                sql += """  contract_industry='""" + case_industry + """' """
        print(sql, '#'*5)
        results  = select_db(sql)


    return render_template('search.html', typelist=typelist,
                 errors=errors, results=results)

if __name__ == '__main__':
    app.run()