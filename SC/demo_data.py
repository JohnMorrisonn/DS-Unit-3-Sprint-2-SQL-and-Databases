import sqlite3

# Open connection to blank database

conn = sqlite3.connect('demo_data.sqlite3')
curs = conn.cursor()

# Remove table if already created as to not create and
# insert data multiple times
curs.execute("DROP TABLE demo")

# Data from the table given in markdown
data = [('g', 3, 9), ('v', 5, 7), ('f', 8, 7)]

# Command to Creat table demo
create_demo_table = """
  CREATE TABLE demo (
    s TEXT,
    X INT,
    y INT
  );
"""

curs.execute(create_demo_table)

# Insert data from data list above into table
for d in data:
    insert_data = """
        INSERT INTO demo
        (s, x, y) VALUES """ + str(d[0:]) + ';'
    curs.execute(insert_data)

conn.commit()


def get_query(query, info_str, curs):
    """
    Execute and display queries
    Add a comment as to what the query is
    Add a line after
    """
    curs.execute(query)
    print(info_str, curs.fetchall(), '\n')

# Query for how many rows in the table

query = "SELECT COUNT(*) FROM demo"
get_query(query, 'How many rows in demo table?', curs)

# How many rows are there where both x and y are at least 5?

query = "SELECT COUNT(*) FROM demo WHERE (x >= 5) AND (y >=5)"
get_query(query, 'How many rows do x and y both have at least 5?', curs)

# How many unique values of y are there?

query = "SELECT COUNT(DISTINCT(y)) FROM demo"
get_query(query, 'How many unique values are in y?', curs)
