import sqlite3

# Open connection to blank database

conn = sqlite3.connect('demo_data.sqlite3')
curs = conn.cursor()

# Remove table if already created
curs.execute("DROP TABLE demo")

data = [('g', 3, 9), ('v', 5, 7), ('f', 8 ,7)]

create_demo_table = """
  CREATE TABLE demo (
    s TEXT,
    X INT,
    y INT
  );
"""

curs.execute(create_demo_table)

for d in data:
    insert_data = """
        INSERT INTO demo
        (s, x, y) VALUES """ + str(d[0:]) + ';'
    curs.execute(insert_data)

conn.commit()

def get_query(query, info_str, curs):
    curs.execute(query)
    print(info_str, curs.fetchall())

# Query for how many rows

query = "SELECT COUNT(*) FROM demo"
get_query(query, 'How many rows in demo table?', curs)

# How many rows are there where both x and y are at least 5?

query = "SELECT COUNT(*) FROM demo WHERE (x >= 5) AND (y >=5)"
get_query(query, 'How many rows do x and y both have at least 5?', curs)

# How many unique values of y are there?

query = "SELECT COUNT(DISTINCT(y)) FROM demo"
get_query(query, 'How many unique values are in y?', curs)