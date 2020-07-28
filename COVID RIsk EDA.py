#!/usr/bin/env python
# coding: utf-8

# In[4]:


import psycopg2
#import pandas as pd
import os
#from config import Config
import matplotlib.pyplot as plt
import pandas as pd


# declare a new PostgreSQL connection object
conn = psycopg2.connect("host=covid19.c9opif8xcrgf.us-east-1.rds.amazonaws.com dbname=covid19 user= password=")
folder = os.path.join(os.getcwd(), 'data','NYTimes')
print('The Folder is: ' +folder)


# In[15]:



df_county = pd.read_sql('SELECT * FROM ny_us_counties', conn)


# In[16]:


df_county.head()


# In[17]:


# general information about the dataframe
print(df_county.info())


# In[18]:


#printing out column names
print(df_county.columns)


# In[ ]:


#date column


# In[19]:


df_county.describe()


# In[20]:


df_county.describe(include=['object', 'bool'])


# In[ ]:



series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
series.plot()
pyplot.show()


series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
series.plot()
pyplot.show()


# In[ ]:




def load_data(schema, table):

    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)


# In[ ]:


df.hist(column='cases')


# In[ ]:


df.hist(column='death')


# In[ ]:





# In[ ]:


df.plot(kind='bar',x='county',y='death')


# In[9]:


df_state = pd.read_sql('SELECT * FROM csse_covid_19_data_us', conn)


# In[21]:


df_state.info()


# In[22]:


print(df_state.isnull())


# In[10]:


df_state.head()


# In[11]:


df_state.plot(kind='bar',x='province_state',y='deaths')


# In[13]:


df_state.hist(column='deaths')
