import psycopg2
#import pandas as pd
import os
#from config import Config

conn = psycopg2.connect("host=covid19.c9opif8xcrgf.us-east-1.rds.amazonaws.com dbname=covid19 user=covid19 password=covid2019")
folder = os.path.join(os.getcwd(), 'data','CSSE')
print('The Folder is: ' +folder)

for subdir, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith("csv"):
            print('The file is ' +file)
            filepath = subdir + os.sep + file
            print('The complete filepath '+filepath)
            cur = conn.cursor()
            with open(filepath, 'r') as pfile:
                print('importing: '+str(pfile))
                next(pfile)
                cur.copy_from(pfile, 'csse_covid_19_data_us', sep=',', null="")
                conn.commit()
