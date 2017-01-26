    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob,os
import paramiko
import time
import re

from utils.json_utils import utils_json
from page_parser.torrent_info import torrent_info
from utils.multithread.worker import Worker
import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
'''
engine = sqlalchemy.create_engine('mysql://root:021010@192.168.1.75/PRUEBA', echo=False)  # connect to server
engine.execute("USE PRUEBA")  # select new db

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Torrent(Base):
    __tablename__ = 'TORRENT_LINK'
    torrent_id = Column(Integer, primary_key=True, autoincrement=False)
    torrent_group = Column(Integer)
    torrent_url = Column(String(200))
    torrent_name = Column(String(200))
    torrent_link = Column(String(200))
    torrent_size = Column(Float)
    torrent_size_unit = Column(String(2))
    torrent_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return repr(Base())

Base.metadata.create_all(bind=engine)
'''





def get_capitulos():
    returnList=[]
    path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)), os.pardir))
    files = glob.glob(path + "/state/newpct_series/*.json")
    for file in files:
        try:
            tvshow=utils_json.readJSONfile(file)
            for cap in tvshow['capitulos_list']:
                returnList.append(dict(cap))
        except Exception as e:
            print 'ERROR', file, e.message


    return returnList


class ExampleMultithread (Worker):
    def __init__(self,nthreads=1):
        self.nthreads=nthreads
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        self.ssh.connect('192.168.1.75', username='pi', password='021010')

        super ( ExampleMultithread, self ).__init__ ( )

    def _retrive_task(self):
        return get_capitulos()

    def _do(self,task):
        try:
            obj=torrent_info(task,self.ssh)
        except Exception as e:
            print task, e.message


c = ExampleMultithread(5)
