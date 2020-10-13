import json
import sqlite3
# from pprint import pprint


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


def get_json(filename):
    file = 'airbnb.json'
    listing = []
    with open(file, 'r', encoding="utf8") as myfile:
        data = myfile.read()
        listing = json.loads(data)
    return listing


def import_accommodation(listing):
    insert_list = []
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    for i in listing:
        id = i["_id"]
        name = i["name"]
        summary = i["summary"]
        url = i["listing_url"]
        review_score_value = None
        if i['review_scores'] != {}:
            review_score_value = i['review_scores'].get('review_scores_value', None)
        insert_list.append((id, name, summary, url, review_score_value))

    c.executemany("INSERT INTO accommodation (id, name, summary, url, review_score_value)\
                   VALUES (?, ?, ?, ?, ?)", insert_list)
    conn.commit()
    conn.close()
    print('insert ', len(insert_list), ' accommodation')


def import_host(listing):
    insert_list = []
    host_count_dict = {}
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    for i in listing:
        h = i["host"]

        host_count = host_count_dict.get(h['host_id'], None)
        # If a host (with certain host ID) has more than one accommodation,
        # we only store the 1st occurrence
        if host_count is None:
            host_count_dict[h['host_id']] = 1
            insert_list.append((h['host_id'], h['host_url'], h['host_name'],
                                h['host_about'], h['host_location']))
        # else:
        #     print('## host already exitsted, skip', len(insert_list))

    c.executemany("INSERT INTO host (host_id, host_url, host_name, host_about, host_location)\
                   VALUES (?, ?, ?, ?, ?)", insert_list)
    conn.commit()
    conn.close()
    print('insert ', len(insert_list), ' hosts')


def import_host_accommodation(listing):
    insert_list = []
    host_count_dict = {}
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    for i in listing:
        id = i["_id"]
        h = i["host"]

        host_count = host_count_dict.get(h['host_id'], None)
        # If a host (with certain host ID) has more than one accommodation,
        # we only store the 1st occurrence
        if host_count is None:
            host_count_dict[h['host_id']] = 1
            insert_list.append((h['host_id'], id))
        # else:
        #     print('## host_accommodation already exitsted, skip', len(insert_list))

    c.executemany("INSERT INTO host_accommodation (host_id, accommodation_id)\
                   VALUES (?, ?)", insert_list)
    conn.commit()
    conn.close()
    print('insert ', len(insert_list), ' host_accommodation')


def import_reviewer(listing):
    insert_list = []
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    for i in listing:
        reviews = i["reviews"]
        for review in reviews:
            # consider reviewer_id and reveiwer_name combined should be unique,
            # we only store the 1st occurrence
            if (review['reviewer_id'], review['reviewer_name']) not in insert_list:
                insert_list.append((review['reviewer_id'], review['reviewer_name']))

    c.executemany("INSERT INTO reviewer (rid, rname)\
                   VALUES (?, ?)", insert_list)
    conn.commit()
    conn.close()
    print('insert ', len(insert_list), ' reviewers')


def import_review(listing):
    insert_list = []
    reviewer_count_dict = {}
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    for i in listing:
        id = i["_id"]
        reviews = i["reviews"]
        for review in reviews:
            reviewer_count = reviewer_count_dict.get(review['reviewer_id'], None)
            # If a reviewer (with certain reviewer ID) have more than one reviews,
            # only the first occurrence of the reviewer data will be stored in the database.
            if reviewer_count is None:
                d = review['date']['$date']
                # print('d=', d)
                reviewer_count_dict[review['reviewer_id']] = 1
                insert_list.append((review['reviewer_id'], review['comments'], d, id))
            # else:
            #     print('allready exitsted reviewer', len(insert_list))

    c.executemany("INSERT INTO review (rid, comment, datetime, accommodation_id)\
                   VALUES (?, ?, ?, ?)", insert_list)
    conn.commit()
    conn.close()
    print('insert ', len(insert_list), ' reviews')


def import_amenities(listing):
    insert_list = []
    conn = sqlite3.connect("airbnb.db")
    c = conn.cursor()
    for i in listing:
        id = i["_id"]
        ams = i["amenities"]
        # print(ams, ams[0])
        type_count_dict = {}
        for am in ams:
            type_count = type_count_dict.get(am, None)
            # If a reviewer (with certain reviewer ID) have more than one reviews,
            # only the first occurrence of the reviewer data will be stored in the database.
            if type_count is None:
                type_count_dict[am] = 1
                insert_list.append((id, am))
            # else:
            #     print(am, 'allready exitsted amenities', len(insert_list), '#'*10)

    c.executemany("INSERT INTO amenities (accommodation_id, type)\
                   VALUES (?, ?)", insert_list)
    conn.commit()
    conn.close()
    print('insert ', len(insert_list), ' amenities')


def start():
    create_table_schema()
    listing = get_json('airbnb.json')
    import_accommodation(listing)
    import_host(listing)
    import_host_accommodation(listing)
    import_reviewer(listing)
    import_review(listing)
    import_amenities(listing)


if __name__ == "__main__":
    start()
