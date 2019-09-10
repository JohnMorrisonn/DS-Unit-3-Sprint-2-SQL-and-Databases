#!/usr/bin/env python
# coding: utf-8

# ## Load in the buddy dataset

# In[2]:


import pandas as pd
import sqlite3


# In[3]:


# Load in the dataset

buddy = pd.read_csv('buddymove_holidayiq.csv')
buddy.shape


# In[4]:


# Create an SQL connection to a blank dataset

conn = sqlite3.connect('buddymove_holidayiq.sqlite3')


# Put buddy csv into that SQL connection

buddy.to_sql('buddy', con=conn)


# In[5]:


# Create the connection cursor and check that it has the same number of rows

c = conn.cursor()
query = 'SELECT Count(*) FROM buddy'
c.execute(query).fetchall()


# In[6]:


# Take a further look into the data

query = 'SELECT * FROM buddy'
df = pd.read_sql(query, conn)
df


# ### How many users reviewd at least 100 Nature and 100 in shopping?

# In[12]:


query = '''SELECT COUNT('User Id') FROM buddy WHERE (Nature >= 100) & (Shopping >= 100)
'''
c.execute(query).fetchone()


# ### What are the average number of reviews for each category?

# In[33]:


query = '''SELECT AVG(Sports), AVG(Religious), AVG(Nature), AVG(Theatre), AVG(Shopping), AVG(Picnic) FROM buddy
'''
c.execute(query).fetchall()
    

