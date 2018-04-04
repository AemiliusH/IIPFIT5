from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

path = '..//DataBase//DB.sqlite'
engine = create_engine('sqlite:///%s' % path, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Database():
    def __init__(self, hoofdmenu):
        self.hoofdmenu_refrentie = hoofdmenu



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')











