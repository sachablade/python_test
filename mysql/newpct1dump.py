import MySQLdb
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('mysql://root:021010@192.168.1.75/Prueba' , echo=True) # connect to server
engine.execute("USE Prueba") # select new db
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

# Open database connection
db = MySQLdb.connect("192.168.1.75","root","021010","Prueba" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("select distinct processId FROM Prueba.M_PROCESS;")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

# disconnect from server
db.close()