import json
import sqlite3


def create_table_schema():
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS accommodation")
    c.execute('''
        CREATE TABLE accommodation
        (id INTEGER PRIMARY KEY , name text, summary text,
            url text, review_score_value INTEGER)''')

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
            comment text, datetime text, accommodation_id INTEGER,
         CONSTRAINT fk_column
            FOREIGN KEY (accommodation_id) REFERENCES accommodation (id)
            FOREIGN KEY (rid) REFERENCES reviewer (rid)
        )''')

    c.execute("DROP TABLE IF EXISTS amenities")
    c.execute('''
        CREATE TABLE amenities
        (accommodation_id INTEGER, type text,
        PRIMARY KEY (accommodation_id, type)
        CONSTRAINT fk_column
            FOREIGN KEY (accommodation_id) REFERENCES accommodation (id)
        )''')

    c.execute("DROP TABLE IF EXISTS host_accommodation")
    c.execute('''
        CREATE TABLE host_accommodation
        (host_id INTEGER, accommodation_id INTEGER,
        PRIMARY KEY (host_id, accommodation_id)
        CONSTRAINT fk_column
            FOREIGN KEY (host_id) REFERENCES host (host_id)
            FOREIGN KEY (accommodation_id) REFERENCES accommodation (id)

        )''')

    conn.commit()
    conn.close()



def start():
    create_table_schema()



if __name__ == "__main__":
    start()
