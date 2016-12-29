#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob,os
import pickle

import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



def load_pickle(file_name):
    b={}
    try:
        with open(file_name, 'rb') as handle:
            b = pickle.load(handle)
    except:
        pass
    return b


engine = sqlalchemy.create_engine('mysql://root:021010@192.168.1.75/PRUEBA', echo=False)  # connect to server
engine.execute("USE PRUEBA")  # select new db

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class AutoRepr(object):
     def __repr__(self):
         items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
         return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

class Torrent(Base):
    __tablename__ = 'TORRENT_LINK'
    torrent_id = Column(Integer, primary_key=True, autoincrement=False)
    torrent_url = Column(String(200))
    torrent_name = Column(String(200))
    torrent_link = Column(String(200))
    torrent_size = Column(String(5))
    torrent_size_unit = Column(String(2))
    torrent_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return repr(Base())

Base.metadata.create_all(bind=engine)

files=glob.glob(os.getcwd() + "/state/*.p")

for file in files:
    try:
        tvshow=load_pickle(file)
        print tvshow['title'],len(tvshow['capitulos_list']),tvshow['capitulos']
        #if tvshow['title'] == 'Billions':
        max_name=0
        max_link=0
        for cap in tvshow['capitulos_list']:
            if cap.has_key('torrent_link'):
                try:
                    dt = datetime.datetime.strptime(cap['date'], "%d-%m-%Y")
                except:
                    dt = datetime.datetime.utcnow
                existe = session.query(Torrent).filter(Torrent.torrent_id == cap['torrent_link'].__hash__()).count()
                if existe == 0:
                    session.add_all([
                        Torrent(torrent_id=cap['torrent_link'].__hash__(), torrent_url=cap['url'], torrent_name=cap['torrent_title'], torrent_link=cap['torrent_link'],
                                torrent_size=cap['size'][0], torrent_size_unit=cap['size'][1], torrent_date=dt)
                    ])

                else:
                    pass
        session.commit()
    except:
        print 'ERRROR ' + tvshow['title']
        raise

