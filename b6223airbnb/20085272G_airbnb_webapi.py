from flask import Flask
from flask import request
from flask import jsonify
import sqlite3
from collections import defaultdict 


app = Flask(__name__)
# app.config['DEBUG'] = True
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
        # print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def review_list_to_json(viewdata):
    reviews = []
    for item in viewdata:
        reviews.append({"Accommodation ID": item[3],
                        "Comment": item[1],
                        "DateTime": item[2],
                        "Reviewer ID": item[0],
                        "Reviewer Name": item[4]})
    r = {
    "Count": len(viewdata),
    "Reviews":reviews
    }
    # return jsonify(results = r)
    return jsonify(r)


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
        # print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def reviewer_list_to_json(viewdata):
    reviewers = []
    for item in viewdata:
        reviewers.append({"Review Count": item[0],
                        "Reviewer ID": item[1],
                        "Reviewer Name": item[2]})
    r = {
    "Count": len(viewdata),
    "Reviewers":reviewers
    }
    return jsonify(r)


def select_reviews_per_reviewer(reviewer_id):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        sql = """SELECT  accommodation_id, comment, r2.datetime, r3.rid, r3.rname  
                from review r2 join reviewer r3 on
                r2.rid = r3.rid 
                where r2.rid = """ + reviewer_id + """ order by datetime desc """

        # print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def reviews_per_reviewer_list_to_json(viewdata):
    reviews = []
    for item in viewdata:
        reviews.append({"Accommodation ID": item[0],
                        "Comment": item[1],
                        "DateTime": item[2]})
    r = {
    "Reviewer ID": viewdata[0][3],
    "Reviewer Name": viewdata[0][4],
    "Reviews":reviews
    }
    return jsonify(r)


def select_hosts(sort_by_accommodation_count):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        sql = """SELECT  COUNT(*) TotalCount, 
                 h.host_about ,h.host_id ,h.host_location ,h.host_name ,h.host_url 
                FROM    host h
                INNER JOIN host_accommodation ha
                ON h.host_id = ha.host_id 
                GROUP   BY ha.host_id """

        if sort_by_accommodation_count == 'ascending':
            sql += """ order by TotalCount asc, h.host_id asc """
        elif sort_by_accommodation_count == 'descending':
            sql += """ order by TotalCount desc, h.host_id asc """
        # print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def host_list_to_json(viewdata):
    hosts = []
    for item in viewdata:
        hosts.append({"Accommodation Count": item[0],
                        "Host About": item[1],
                        "Host ID": item[2],
                        "Host Location": item[3],
                        "Host Name": item[4],
                        "Host Url": item[5]})
    r = {
    "Count": len(viewdata),
    "Hosts":hosts
    }
    return jsonify(r)

def select_hosts_per_hostid(host_id):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        sql = """SELECT  a.id, a.name ,
                h.host_about ,h.host_id ,h.host_location ,h.host_name ,h.host_url 
                FROM    host h
                        INNER JOIN host_accommodation ha
                            ON h.host_id = ha.host_id 
                           INNER  JOIN accommodation a on
                           a.id = ha.accommodation_id 
                where h.host_id = """ +  host_id +  """ order by a.id asc; """

        # print(sql)
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def hosts_per_hostid_list_to_json(viewdata):
    accommodations = []
    for item in viewdata:
        accommodations.append({"Accommodation ID": item[0],
                        "Accommodation Name": item[1]})
    r = {
    "Accommodation": accommodations,
    "Accommodation Count": len(viewdata),
    "Host About": item[2],
    "Host ID": item[3],
    "Host Location": item[4],
    "Host Name": item[5],
    "Host Url": item[6]
    }
    return jsonify(r)


def select_accommodations_partI(min_review_score_value):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        if min_review_score_value is not None:
            sql = """select a.name, a.summary, a.url ,
                    h.host_about ,h.host_id ,h.host_location ,h.host_name,
                    a.id, COUNT(*) ReviewCount, a.review_score_value 
                    from accommodation a 
                    inner join review r 
                    on a.id  = r.accommodation_id 
                            inner join host_accommodation ha on a.id  = ha.accommodation_id 
                            inner join host h on h.host_id = ha.host_id 
                        where a.review_score_value =""" + min_review_score_value + """
                    GROUP   BY r.accommodation_id  """
        else:
            sql = """select a.name, a.summary, a.url ,
                    h.host_about ,h.host_id ,h.host_location ,h.host_name,
                    a.id, COUNT(*) ReviewCount, a.review_score_value 
                    from accommodation a 
                    inner join review r 
                    on a.id  = r.accommodation_id 
                            inner join host_accommodation ha on a.id  = ha.accommodation_id 
                            inner join host h on h.host_id = ha.host_id 
                    GROUP   BY r.accommodation_id """         
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def select_accommodations_partII(amenities):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()
        if amenities is not None:
            sql = """select a1.accommodation_id , a1."type" from amenities a1 where a1.accommodation_id  in (
                        select   a2.accommodation_id  from amenities a2 
                        where a2."type" == '""" + amenities +  """' 
                        ) order by a1."type" asc; """
        else:
            sql = """ select a2.accommodation_id, a2."type"   from amenities a2 order by a2."type" asc; """
        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def select_accommodations(min_review_score_value, amenities):
    t1 = select_accommodations_partI(min_review_score_value)
    t2 = select_accommodations_partII(amenities)
    if min_review_score_value is not None and len(t1) == 0:
        return []
    if amenities is not None and len(t2) == 0:
        return []

    res = defaultdict(list) 
    for i, j in t2: 
        res[i].append(j)
    # print("The merged dictionary is : " + str(dict(res)))
    combined = []
    for record in t1:

        myamenities = res[record[7]]
        if amenities is not None:
            if len(myamenities) > 0:
                new = record + (myamenities, )
                combined.append(new)
        else:
            new = record + (myamenities, )
            combined.append(new)

    return combined


def accommodations_list_to_json(viewdata):
    accommodations = []
    for item in viewdata:
        accommodations.append(
            {
            "Accommodation": {
             "Name": item[0],
             "Summary": item[1],
             "url": item[2]
            },
            "Amenities": item[10],
            "Host": {
                "About": item[3],
                "ID": item[4],
                "Location": item[5],
                "Name": item[6]
                },
            "ID": item[7],
            "Review Count": item[8],
            "Review Score Value": item[9]

            })
    r = {
    "Accommodations": accommodations
    }
    return jsonify(r)


def select_single_accommodation_partI(accommodation_id):
    viewdata = []
    with sqlite3.connect("airbnb.db") as db:
        cursor = db.cursor()

        sql = """
            select a.id , a.name , a.review_score_value , r.comment ,r.datetime ,r.rid , r2.rname,
            a.summary , a.url 
            from accommodation a 
            inner join review r 
            on a.id  = r.accommodation_id 
            inner join reviewer r2 
            on r.rid  = r2.rid 
            where a.id ="""  + accommodation_id

        cursor.execute(sql)
        viewdata = cursor.fetchall()
        # print('#'*10, len(viewdata),viewdata[0])
    db.commit()
    return viewdata


def select_single_accommodation(accommodation_id):
    t1 = select_single_accommodation_partI(accommodation_id)
    t2 = select_accommodations_partII(None)
    res = defaultdict(list) 
    for i, j in t2: 
        res[i].append(j)
    # print("The merged dictionary is : " + str(dict(res)))
    myamenities = res[int(accommodation_id)]

    combined = []
    for record in t1:
        
        new = record + (myamenities, )
        combined.append(new)
    return combined    


def single_accommodation_list_to_json(viewdata):
    reviews = []
    for item in viewdata:
        reviews.append(
            {
            "Comment":  item[3],
            "DateTime": item[4],
            "Reviewer ID": item[5],
            "Reviewer Name": item[6]
            })
    r = {
    "Accommodation ID": viewdata[0][0],
    "Accommodation Name": viewdata[0][1],
    "Amenities": viewdata[0][9],
    "Review Score Value": viewdata[0][2],
    "Reivews": reviews,
    "Summary": viewdata[0][7],
    "URL": viewdata[0][8]
    }
    return jsonify(r)


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


@app.route('/airbnb/hosts/')
def hosts():
    sort_by_accommodation_count = request.args.get('sort_by_accommodation_count')
    v = select_hosts(sort_by_accommodation_count)
    j = host_list_to_json(v)
    return j, 200


@app.route('/airbnb/hosts/<host_id>')
def hosts_per_hostid(host_id):
    v = select_hosts_per_hostid(host_id)
    if len(v) > 0:
        j = hosts_per_hostid_list_to_json(v)
        return j, 200
    else:
        return { "Reasons": [ {"Message": "Host not found"}]}, 404


@app.route('/airbnb/accommodations/')
def accommodations():
    min_review_score_value = request.args.get('min_review_score_value')
    amenities = request.args.get('amenities')
    print('amenities=', amenities)
    v = select_accommodations(min_review_score_value, amenities)
    if len(v) > 0:
        j = accommodations_list_to_json(v)
        return j, 200
    else:
        return { "Reasons": [ {"Message": "Accommodation not found"}]}, 404


@app.route('/airbnb/accommodations/<accommodation_id>')
def single_accommodation(accommodation_id):
    v = select_single_accommodation(accommodation_id)
    if len(v) > 0:
        j = single_accommodation_list_to_json(v)
        return j, 200
    else:
        return { "Reasons": [ {"Message": "Accommodation not found"}]}, 404


if __name__ == '__main__':
    app.run()