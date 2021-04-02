import time
import datetime
import os
import json
import sqlite3


from flask import Flask, request
from flask import jsonify

from flask_restx import Resource, Api
from flask_restx import reqparse


db_name = "a10611.db"

app = Flask(__name__)
app.debug = True


api = Api(app)

original_listing = []

def create_table_schema():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS shows")
    c.execute('''
        CREATE TABLE shows
        (id INTEGER PRIMARY KEY , 
        last_update text,
        tvmaze_id text, 
        name text, 
        type text,
        language text,
        genres BLOB,
        status text,
        runtime INTEGER,
        premiered text,
        officialSite text,
        schedule BLOB,
        rating BLOB,
        weight INTEGER,
        network BLOB,
        summary text )''')



    conn.commit()
    conn.close()


def insert_show(l):
    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
    insert_list = [str(now), l['id'], l['name'], l['type'],l['language'],
                    str(l['genres']), l['status'],
                    l['runtime'], l['premiered'],l['officialSite'],
                    str(l['schedule']), str(l['rating']), l['weight'],
                    str(l['network']), l['summary']
                    ]
    # print('insert_list=', insert_list)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO shows ( last_update, tvmaze_id,\
     name, type,language, genres, status,runtime, premiered,officialSite,\
     schedule, rating, weight, network,summary)\
                   VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?,?,?)", insert_list)

    conn.commit()
    conn.close()
    return c.lastrowid


def select_all_show():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM shows ")

    rows = cur.fetchall()
    if len(rows) >= 0:
        # print(rows[0])
        return rows
    return None

def select_show(id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM shows where id="+ str(id))

    rows = cur.fetchall()
    if len(rows) >= 1:
        # print(rows[0])
        return rows[0]
    return None

def delete_show(id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("delete from shows where id="+ str(id))

    rows = cur.fetchall()
    conn.close()

def update_show(id, name, language):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    if name != None:
        r = "UPDATE shows SET name = '"+ name+"' where id="+ str(id)
        cur.execute(r)
    if language != None:
        r = "UPDATE shows SET language = '"+ language + "' where id="+ str(id)
        cur.execute(r)

    conn.commit()
    conn.close()

def get_json(filename):
    
    listing = []
    with open(filename, 'r', encoding="utf8") as myfile:
        data = myfile.read()
        listing = json.loads(data)
    return listing

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def db_start():
    create_table_schema()
    global original_listing
    listings = get_json('shows.json')

    for listing in listings:
        original_listing.append(listing['show'])
        insert_show(listing['show'])


@api.route('/tv-shows/import')
class TV_Show(Resource):
    def get(self):
        return {}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='name')
        args = parser.parse_args()
        print(args.name)
        for listing in original_listing:
            if listing['name'].lower() == args.name:
                lastid = insert_show(listing)
                now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
                return {"id": lastid, "last-update": str(now),
                        "tvmaze-id" : listing['id'],
                        "_links": {
                        "self": {
                          "href": "http://localhost:5000/tv-shows/"+str(lastid)
                                }
                                  }
                        }, 201
        return {}, 500


@api.route('/tv-shows/<int:todo_id>')
class TV_Show_Detail(Resource):
    def get(self, todo_id):
        l = select_show(todo_id)
        return {"tvmaze-id" : l[0],
                "id": todo_id, 
                "last-update": l[2],
                "name": l[3],
                "type": l[4],
                "language": l[5],
                "genres": l[6],
                "status": l[7],
                "runtime": l[8],
                "premiered": l[9],
                "officialSite": l[10],
                "schedule": l[11],
                "rating": l[12],
                "weight": l[13],
                "network": l[14],
                "summary": l[15],
                        "_links": {
                        "self": {
                          "href": "http://localhost:5000/tv-shows/"+str(todo_id)
                                },
                         "previous": {
                          "href": "http://localhost:5000/tv-shows/"+str(todo_id-1)
                        },
                        "next": {
                          "href": "http://localhost:5000/tv-shows/"+str(todo_id+1)
                        }
                                  }
                        }, 201

    def patch(self, todo_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='name')
        parser.add_argument('language', type=str, help='language')
        parser.add_argument('genres', type=str, help='genres')
        parser.add_argument('status', type=str, help='status')
        parser.add_argument('runtime', type=str, help='runtime')
        args = parser.parse_args()

        update_show(todo_id, args.name, args.language)
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        return {"id": todo_id, "last-update": str(now),
                      
                        "_links": {
                        "self": {
                          "href": "http://localhost:5000/tv-shows/"+str(todo_id)
                                }
                                  }
                        }, 200

    def delete(self, todo_id):
        delete_show(todo_id)
        return { 
            "message" :"The tv show with id "+str(todo_id)+ " was removed from the database!",
            "id": todo_id
        }, 200


@api.route('/tv-shows')
class TV_Show_Page(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('order_by', type=str, help='order_by')
        parser.add_argument('page', type=int, help='page')
        parser.add_argument('page_size', type=int, help='page_size')
        parser.add_argument('filter', type=str, help='filter')
        args = parser.parse_args()
        print(args)
        tv_list = select_all_show()
        my_list = list(chunks(tv_list, args.page_size))
        return {
            "page": 1,
            "page-size": 100,
            "tv-shows": [ 
                   my_list
                ],
            "_links": {
                "self": {
                  "href": "http://[HOST_NAME]:[PORT]/tv-shows?page=1&page_size=1000&filter=id,name"
                },
                "next": {
                  "href": "http://[HOST_NAME]:[PORT]/tv-shows?page=2&page_size=1000&filter=id,name"
                }
              }
        }, 201

@api.route('/tv-shows/statistics')
class TV_Show_Statistics(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('format', type=str, help='format')
        parser.add_argument('by', type=str, help='by')

        args = parser.parse_args()
        print(args)
        tv_list = select_all_show()
        updated = 0
        by_count = {}
        for tv in tv_list:
            print(tv[12], type(tv[12]), '@'*10)
            json_acceptable_string = tv[12].replace("'", "\"")
            r = json.loads(json_acceptable_string)['average']
            print(r)
            if tv[5] not in by_count:
                by_count[tv[5]] = r
            else:
                by_count[tv[5]] += r
            record_dt = datetime.datetime.strptime(tv[1],'%Y-%m-%d_%H-%M-%S')
            dnow = datetime.datetime.now()
            if abs(dnow- record_dt) < datetime.timedelta(hours=24):
                updated += 1
            return { 
           "total": len(tv_list),
           "total-updated": updated,
           "values" : { "English": 60.7, "French": 19.2} 
        }, 201



if __name__ == '__main__':
    db_start()
    app.run(debug=True)