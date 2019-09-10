#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import sqlite3
import numpy
import sys


# ## The RPG Dataset

# In[105]:


conn = sqlite3.connect('rpg_db (1).sqlite3')


# In[106]:


c = conn.cursor()
c.execute('SELECT * FROM charactercreator_character').fetchall()
conn.commit()


# In[11]:


query = 'SELECT * FROM charactercreator_character'

pd.read_sql(query, conn)


# ### How many characters are in the dataset?

# In[19]:


# How many characters are in the dataset

c.execute('SELECT COUNT(character_id) FROM charactercreator_character')
result = c.fetchone()
result


# ### How many tables are in the dataset?

# In[40]:


def get_sql_tables(db_con):
    c = db_con.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()

get_sql_tables(conn)


# ### How man characters of each subclass?

# In[75]:


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


# In[72]:


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


# ### How many items are there total?

# In[83]:


# How many total items?

query = 'SELECT COUNT(*) FROM armory_item'
c.execute(query).fetchone()


# ### And Weapons?

# In[103]:


# How many are weapons and how many are not

query_weapon = 'SELECT item_id FROM armory_item INNER JOIN armory_weapon ON item_id = item_ptr_id'
print('Weapon count', len(c.execute(query_weapon).fetchall()))

query_non_weapon = 'SELECT item_id FROM armory_item EXCEPT SELECT item_ptr_id FROM armory_weapon'
print('Not weapon', len(c.execute(query_non_weapon).fetchall()))


# ### How many items and weapons per character?

# In[82]:


# How many items does each character have

query = 'SELECT character_id as char_id, COUNT(item_id) FROM charactercreator_character_inventory GROUP BY character_id LIMIT 20'
df = pd.read_sql(query, conn)
df


# In[117]:


# How many Weapons does each character have

query = 'SELECT character_id, COUNT(item_id) FROM charactercreator_character_inventory INNER JOIN armory_weapon ON item_id = item_ptr_id GROUP BY character_id LIMIT 20 '
df = pd.read_sql(query, conn)
df


# ### What is the average number of items and weapons carried?

# In[124]:


# How many items on Average does each character have

query = '''SELECT AVG(item_count) FROM
(SELECT character_id, COUNT(item_id) as item_count FROM charactercreator_character_inventory GROUP BY character_id) '''
df = pd.read_sql(query, conn)
df


# In[125]:


# How many weapons on Average does each character have
# This results in the average from those WITH weapons. Not those without weapons

query = '''SELECT AVG(item_count) FROM
(SELECT character_id, COUNT(item_id) as item_count FROM charactercreator_character_inventory INNER JOIN armory_weapon ON item_id = item_ptr_id GROUP BY character_id) '''
df = pd.read_sql(query, conn)
df


# In[126]:


# How many weapons on Average does each character have, INCLUDING those without weapons

query = '''SELECT AVG(wc) FROM (SELECT cci.character_id as `Character Id`, COUNT(aw.item_ptr_id) as wc
FROM charactercreator_character_inventory as cci INNER JOIN armory_item as ai ON cci.item_id = ai.item_id
LEFT JOIN armory_weapon as aw ON ai.item_id = aw.item_ptr_id
GROUP BY cci.character_id)
'''
df = pd.read_sql(query,conn)
df

