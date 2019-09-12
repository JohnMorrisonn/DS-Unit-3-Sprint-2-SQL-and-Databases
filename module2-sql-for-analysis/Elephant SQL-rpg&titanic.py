#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install psycopg2-binary')


# In[2]:


import psycopg2
import os

# In[3]:

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

dbname = os.environ.get('dbname')
user = os.environ.get('user')
password = os.environ.get('password')
host = os.environ.get('host')


# In[61]:


pg_conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host)


# In[17]:


pg_curs = pg_conn.cursor()


# In[6]:


get_ipython().system('pip install wget')


# In[7]:


import wget
wget.download('https://github.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/blob/master/module1-introduction-to-sql/rpg_db.sqlite3?raw=true')


# In[8]:


import sqlite3


# In[9]:


sl_conn = sqlite3.connect('rpg_db.sqlite3')


# In[10]:


sl_curs = sl_conn.cursor()


# In[11]:


characters = sl_curs.execute('SELECT * FROM charactercreator_character;').fetchall()


# In[12]:


sl_curs.execute('PRAGMA table_info(charactercreator_character);').fetchall()


# In[13]:


create_character_table = """
  CREATE TABLE charactercreator_character (
    character_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    level INT,
    exp INT,
    hp INT,
    strength INT,
    intelligence INT,
    dexterity INT,
    wisdom INT
  );
"""


# In[18]:


pg_curs.execute(create_character_table)


# In[19]:


show_tables = """
SELECT
   *
FROM
   pg_catalog.pg_tables
WHERE
   schemaname != 'pg_catalog'
AND schemaname != 'information_schema';
"""
pg_curs.execute(show_tables)
pg_curs.fetchall()


# In[20]:


for character in characters:
  insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ';'
  # print(insert_character)
  pg_curs.execute(insert_character)


# In[21]:


pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_curs.fetchall()


# In[22]:


# We can see it from this cursor - but not elephantsql.com!
# We have to commit
pg_curs.close()
pg_conn.commit()


# In[23]:


# OK, we can see it in elephantsql.com now
# But let's also check programmatically
pg_curs = pg_conn.cursor()  # Make a new cursor
pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_characters = pg_curs.fetchall()


# In[24]:


for character, pg_character in zip(characters, pg_characters):
  assert character == pg_character


# ## Titanic

# In[25]:


import pandas as pd


# In[26]:


df = pd.read_csv('Titanic.csv')
df['Name'] = df['Name'].str.replace("'", "")


# In[27]:


t_conn = sqlite3.connect('Titanic.sqlite3')
df.to_sql('Titanic', con=t_conn, if_exists='replace')


# In[28]:


t_curs = t_conn.cursor()


# In[29]:


t_curs.execute('PRAGMA table_info(Titanic);').fetchall()


# In[58]:


create_titanic_table = """
  CREATE TABLE titanic_data (
    index SERIAL PRIMARY KEY,
    Survived INTEGER,
    Pclass INTEGER,
    Name TEXT,
    Sex TEXT,
    Age REAL,
    Siblings_Spouses_Aboard INTEGER,
    Parents_Children_Aboard INTEGER,
    Fare FLOAT
  );
"""


# In[62]:


pg_curs2 = pg_conn.cursor()


# In[63]:


pg_curs2.execute(create_titanic_table)


# In[64]:


persons = t_curs.execute('SELECT * FROM Titanic;').fetchall()


# In[65]:


for person in persons:
    insert_person = """
        INSERT INTO titanic_data
        (index, Survived, Pclass, Name, Sex, Age, Siblings_Spouses_Aboard, Parents_Children_Aboard, Fare)
        VALUES """ + str(person[0:]) + ';'
    pg_curs2.execute(insert_person)


# In[66]:


pg_curs2.close()
pg_conn.commit()


# In[67]:


pg_curs = pg_conn.cursor()  # Make a new cursor
pg_curs.execute('SELECT * FROM titanic_data;')
pg_persons = pg_curs.fetchall()


# In[68]:


for person, pg_person in zip(persons, pg_persons):
    assert person == pg_person

