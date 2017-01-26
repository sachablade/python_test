
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlalchemy
import pandas as pd
from utils.datetime_utils import datetime_utils
from datetime import date
import collections

engine = sqlalchemy.create_engine('mysql://root:021010@192.168.1.75/PRUEBA', echo=False)  # connect to server
engine.execute("USE PRUEBA")

list_results=[]
start_date = date(2016, 1, 8)
end_date = date(2017, 1, 9)
for single_date in datetime_utils.daterange(start_date, end_date):
    print single_date.strftime("%Y-%m-%d 00:00:00")
    df_single = pd.read_sql(
        sql="SELECT torrent_group FROM PRUEBA.TORRENT_LINK WHERE torrent_date='"+single_date.strftime("%Y-%m-%d 00:00:00")+"' GROUP BY torrent_group",
        con=engine)

    df_total = pd.read_sql(
        sql="SELECT  torrent_group,  MAX(torrent_date) AS max_date, DATEDIFF(DATE_FORMAT('"+single_date.strftime("%Y-%m-%d 00:00:00")+"','%%Y-%%m-%%d %%T'), MAX(torrent_date)) AS days FROM  "
            "PRUEBA.TORRENT_LINK WHERE    torrent_date < '"+single_date.strftime("%Y-%m-%d 00:00:00")+"' GROUP BY torrent_group",
        con=engine)
    print df_total[df_total.torrent_group.isin(df_single['torrent_group'].tolist())]['days'].tolist()
    list_results+=df_total[df_total.torrent_group.isin(df_single['torrent_group'].tolist())]['days'].tolist()

model=collections.Counter(list_results)
df_model=pd.DataFrame()
df_model['value']=model.keys()
df_model['VALOR']=model.values()




