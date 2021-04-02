import time
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
    print('insert_list=', insert_list)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO shows ( last_update, tvmaze_id,\
     name, type,language, genres, status,runtime, premiered,officialSite,\
     schedule, rating, weight, network,summary)\
                   VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?,?,?)", insert_list)

    conn.commit()
    conn.close()
    return c.lastrowid


def get_json(filename):
    
    listing = []
    with open(filename, 'r', encoding="utf8") as myfile:
        data = myfile.read()
        listing = json.loads(data)
    return listing


def db_start():
    create_table_schema()
    global original_listing
    listings = get_json('shows.json')

    for listing in listings:
        original_listing.append(listing['show'])


@api.route('/tv-shows/import')
class TV_Show(Resource):
    def get(self):
        return {'hello': 'world'}

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


if __name__ == '__main__':
    db_start()
    app.run(debug=True)