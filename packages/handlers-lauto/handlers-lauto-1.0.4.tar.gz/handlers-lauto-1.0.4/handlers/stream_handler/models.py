from sqlalchemy import Boolean,JSON,Column,DateTime, Float, ForeignKey, Integer, String, Time, text,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

Base = declarative_base()

metadata = Base.metadata
engine = create_engine('sqlite:///stream_log.db')
Session = sessionmaker(bind=engine)
session = Session()

class StreamLogStructure(Base):
	__tablename__ = 'stream_log'
	id = Column(Integer,primary_key=True)
	data_entrada = Column(DateTime)
	levelname = Column(String)
	name = Column(String)
	pathname = Column(String)
	lineno = Column(String)
	msg = Column(String)
	args = Column(String)
	exc_info = Column(String)
	exc_text = Column(String)
	stack_info = Column(String)

	def getMessage(self):
		return self.msg

class StreamLog:
	data_entrada:datetime.datetime
	levelname:str
	name:str
	pathname:str
	lineno:str
	msg:str
	args:str
	exc_info:str
	exc_text:str
	stack_info:str

	def __init__(self,**kwargs):
		for arg in kwargs.keys():
			setattr(self,arg,kwargs[arg])

	def getMessage(self):
		return self.msg