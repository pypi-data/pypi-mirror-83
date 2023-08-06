from sqlalchemy import Boolean,JSON,Column,DateTime, Float, ForeignKey, Integer, String, Time, text,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

metadata = Base.metadata
engine = create_engine('sqlite:///rotating_file_log.db')
Session = sessionmaker(bind=engine)
session = Session()

class RotatingFileLogStructure(Base):
	__tablename__ = 'rotating_file_log'
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