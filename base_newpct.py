from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class tvshow(Base):
    __tablename__ = '_tvshow'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_date = Column(DateTime, default=func.now())

