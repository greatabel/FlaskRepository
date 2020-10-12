# import json
import sqlite3
# from pprint import pprint


def create_table_schema():
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS accomodation")
    c.execute('''
        CREATE TABLE accomodation
        (id INTEGER PRIMARY KEY , name text, summary text,
            url text review_score_value INTEGER)''')

    c.execute("DROP TABLE IF EXISTS reviewer")
    c.execute('''
        CREATE TABLE reviewer
        (rid INTEGER PRIMARY KEY , rname text)''')

    c.execute("DROP TABLE IF EXISTS host")
    c.execute('''
        CREATE TABLE host
        (host_id INTEGER PRIMARY KEY , host_url text,
            host_name text, host_about text, host_location text)''')

    c.execute("DROP TABLE IF EXISTS review")
    c.execute('''
        CREATE TABLE review
        (id INTEGER PRIMARY KEY autoincrement, rid INTEGER,
            comment text, datetime text, accomodation_id INTEGER,
         CONSTRAINT fk_column
            FOREIGN KEY (accomodation_id) REFERENCES accomodation (id)
            FOREIGN KEY (rid) REFERENCES reviewer (rid)
        )''')

    c.execute("DROP TABLE IF EXISTS amenities")
    c.execute('''
        CREATE TABLE amenities
        (accomodation_id INTEGER, type text,
        PRIMARY KEY (accomodation_id, type)
        CONSTRAINT fk_column
            FOREIGN KEY (accomodation_id) REFERENCES accomodation (id)
        )''')

    c.execute("DROP TABLE IF EXISTS host_accomodation")
    c.execute('''
        CREATE TABLE host_accomodation
        (host_id INTEGER, accomodation_id INTEGER,
        PRIMARY KEY (host_id, accomodation_id)
        CONSTRAINT fk_column
            FOREIGN KEY (host_id) REFERENCES host (host_id)
            FOREIGN KEY (accomodation_id) REFERENCES accomodation (id)

        )''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table_schema()
