# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'module1-introduction-to-sql'))
	print(os.getcwd())
except:
	pass

#%%
import pandas as pd
import sqlite3
import numpy
import sys


#%%
conn = sqlite3.connect('rpg_db.sqlite3')


#%%
c = conn.cursor()
c.execute('SELECT * FROM charactercreator_character').fetchall()
conn.commit()


#%%
query = 'SELECT * FROM charactercreator_character'

pd.read_sql(query, conn)


#%%
# How many characters are in the dataset

c.execute('SELECT COUNT(character_id) FROM charactercreator_character')
result = c.fetchone()
result


#%%
def get_sql_tables(db_con):
    c = db_con.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()

get_sql_tables(conn)


#%%
# How many of each specific subclass

sub_class = ['charactercreator_cleric',
 'charactercreator_fighter',
 'charactercreator_mage',
 'charactercreator_thief',]

def get_subclass_count(db_con, tables):
    c = db_con.cursor()
    c.execute('SELECT COUNT(character_ptr_id) FROM {}'.format(tables))
    return c.fetchone()

for DB in sub_class:
    print(DB, get_subclass_count(conn, DB))


#%%
# Alternative way

query_cleric = 'SELECT COUNT(*) FROM charactercreator_character AS cc INNER JOIN charactercreator_cleric AS cleric ON cc.character_id = cleric.character_ptr_id'
c.execute(query_cleric)
result = c.fetchone()
print('cleric', result)

query_mage = 'SELECT COUNT(*) FROM charactercreator_character AS cc INNER JOIN charactercreator_mage AS mage ON cc.character_id = mage.character_ptr_id'
c.execute(query_mage)
result = c.fetchone()
print('mage', result)

query_fighter = 'SELECT COUNT(*) FROM charactercreator_character AS cc INNER JOIN charactercreator_fighter AS fighter ON cc.character_id = fighter.character_ptr_id'
c.execute(query_fighter)
result = c.fetchone()
print('fighter', result)

query_thief = 'SELECT COUNT(*) FROM charactercreator_character AS cc INNER JOIN charactercreator_thief AS thief ON cc.character_id = thief.character_ptr_id'
c.execute(query_thief)
result = c.fetchone()
print('thief', result)


#%%
# How many total items?

query = 'SELECT COUNT(*) FROM armory_item'
c.execute(query).fetchone()


#%%
# How many are weapons and how many are not

query_weapon = 'SELECT item_id FROM armory_item INNER JOIN armory_weapon ON item_id = item_ptr_id'
print('Weapon count', len(c.execute(query_weapon).fetchall()))

query_non_weapon = 'SELECT item_id FROM armory_item EXCEPT SELECT item_ptr_id FROM armory_weapon'
print('Not weapon', len(c.execute(query_non_weapon).fetchall()))


#%%
# How many items does each character have

query = 'SELECT character_id as char_id, COUNT(item_id) FROM charactercreator_character_inventory GROUP BY character_id LIMIT 20'
df = pd.read_sql(query, conn)
df


