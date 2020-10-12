from flask import Flask
from flask import request
from flask import jsonify
import sqlite3


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False

def select_reviews(start, end):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        sql = """SELECT r.rid, r.comment , r.datetime , r.accommodation_id, e.rname 
                            FROM review r INNER JOIN reviewer e
                                          ON r.rid = e.rid """
        if start is not None and end is None:
            sql += """ WHERE r.datetime > '""" + start + """'"""
        elif start is None and end is not None:
            sql += """ WHERE r.datetime < '""" + end + """'"""
        elif start is not None and end is not None:
            sql += """WHERE r.datetime > '""" + start + """' and r.datetime < '""" + end + """'"""
        sql += """ order by r.datetime desc , r.rid asc """
        print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def list_to_json(viewdata):
    reviews = []
    for item in viewdata:
        reviews.append({'Accommodation ID': item[3],
                        'Comment': item[1],
                        'DateTime': item[2],
                        'Reviewer ID': item[0],
                        'Reviewer Name': item[4]})
    r = {
    "Count": len(viewdata),
    "Reviews":reviews
    }
    return jsonify(results = r)

@app.route('/mystudentID/')
def hello():
    return {"studentID": "20085272G"}, 200


@app.route('/airbnb/reviews/')
def reviews():
    start = request.args.get('start')
    end = request.args.get('end')

    v = select_reviews(start, end)
    j = list_to_json(v)
    return j, 200



if __name__ == '__main__':
    app.run()