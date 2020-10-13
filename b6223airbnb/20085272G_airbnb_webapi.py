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


def review_list_to_json(viewdata):
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


def select_reviewers(sort_by_review_count):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        sql = """SELECT  COUNT(*) TotalCount, 
                        rv.rid , 
                        r.rname 
                FROM    reviewer r 
                        INNER JOIN review rv
                            ON r.rid = rv.rid 
                GROUP   BY rv.rid """

        if sort_by_review_count == 'ascending':
            sql += """ order by TotalCount asc, rv.rid asc """
        elif sort_by_review_count == 'descending':
            sql += """ order by TotalCount desc,  rv.rid asc """
        print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def reviewer_list_to_json(viewdata):
    reviewers = []
    for item in viewdata:
        reviewers.append({'Review Count': item[0],
                        'Reviewer ID': item[1],
                        'Reviewer Name': item[2]})
    r = {
    "Count": len(viewdata),
    "Reviewers":reviewers
    }
    return jsonify(results = r)


def select_reviews_per_reviewer(reviewer_id):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        sql = """SELECT  accommodation_id, comment, r2.datetime, r3.rid, r3.rname  
                from review r2 join reviewer r3 on
                r2.rid = r3.rid 
                where r2.rid = """ + reviewer_id + """ order by datetime desc """

        print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata

def reviews_per_reviewer_list_to_json(viewdata):
    reviews = []
    for item in viewdata:
        reviews.append({'Accommodation ID': item[0],
                        'Comment': item[1],
                        'DateTime': item[2]})
    r = {
    "Reviewer ID": viewdata[0][3],
    "Reviewer Name": viewdata[0][4],
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
    j = review_list_to_json(v)
    return j, 200


@app.route('/airbnb/reviewers/')
def reviewers():
    sort_by_review_count = request.args.get('sort_by_review_count')
    v = select_reviewers(sort_by_review_count)
    j = reviewer_list_to_json(v)
    return j, 200


@app.route('/airbnb/reviewers/<reviewer_id>')
def reviews_per_reviewer(reviewer_id):
    v = select_reviews_per_reviewer(reviewer_id)
    if len(v) > 0:
        j = reviews_per_reviewer_list_to_json(v)
        return j, 200
    else:
        return { "Reasons": [ {"Message": "Reviewer not found"}]}, 404


if __name__ == '__main__':
    app.run()