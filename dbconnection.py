#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import psycopg2
connection = psycopg2.connect(
    host = 'NEED HOST',
    port = 5432,
    user = 'NEED USER',
    password = 'NEED PASSWORD',
    database='database-1'
    )
cursor=connection.cursor()
