import sqlite3


def create_table_schema():
    conn = sqlite3.connect("legaltext.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS reference")
    c.execute('''
        CREATE TABLE reference
        (id INTEGER PRIMARY KEY autoincrement, title text, content text,
            case_court text, case_year text, case_id text,
            case_cause text, case_industry text)''')

    c.execute("DROP TABLE IF EXISTS memo")
    c.execute('''
        CREATE TABLE memo
        (id INTEGER PRIMARY KEY autoincrement, title text, content text,
            memo_issue text, memo_year text, meomo_industry text)''')

    c.execute("DROP TABLE IF EXISTS evidence")
    c.execute('''
        CREATE TABLE evidence
        (id INTEGER PRIMARY KEY autoincrement, title text, content text,
            evidence_cause text, evidence_plaintiff INTEGER, evidence_nation text,
            evidence_industry text, evidence_court text)''')

    c.execute("DROP TABLE IF EXISTS contract")
    c.execute('''
        CREATE TABLE contract
        (id INTEGER PRIMARY KEY autoincrement, title text, content text,
            contract_type text, contract_language text, contract_amount INTEGER,
            contract_position text, contract_industry text)''')

    conn.commit()
    conn.close()



def start():
    create_table_schema()



if __name__ == "__main__":
    start()
