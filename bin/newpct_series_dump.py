    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob,os
from utils.json_utils import utils_json

import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

path=os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__)), os.pardir))

files=glob.glob(path + "/state/newpct_series/*.json")

for file in files:
    try:
        tvshow=utils_json.readJSONfile(file)
        max_name=0
        max_link=0
        for cap in tvshow['capitulos_list']:
            if cap.has_key('torrent_link'):
                if not cap.has_key('date'):
                    dt = datetime.datetime.utcnow
                else:
                    try:
                        dt = datetime.datetime.strptime(cap['date'], "%d-%m-%Y")
                    except:
                        dt = datetime.datetime.utcnow

                existe = session.query(Torrent).filter(Torrent.torrent_id == cap['id']).count()
                if existe == 0:
                    session.add_all([
                        Torrent(torrent_id=cap['id'], torrent_url=cap['url'], torrent_name=cap['title'], torrent_link=cap['torrent_link'],torrent_group=tvshow['id'],
                                torrent_size=cap['size'], torrent_size_unit=cap['unit'], torrent_date=dt)
                    ])
                else:
                    if cap['title'] in ['Descubriendo a Nina']:
                        print 'error en: ' + file
                        print e.message
                        os.remove(file)
                    pass
        session.commit()
    except Exception as e:
        session.rollback()
        print 'error en: ' + file
        print e.message
        os.remove(file)


