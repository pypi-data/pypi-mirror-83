from logging import StreamHandler
from handlers.stream_handler.models import *
import datetime
import ast
import pytz
from collections import namedtuple

class ScreenHandler(StreamHandler):
	def __init__(self,save:bool=True):
		StreamHandler.__init__(self)
		self.save = save
		if self.save:
			metadata.create_all(engine)

	def sendToStream(self,element):
		try:
			aux = ast.literal_eval(element.msg)
			element.msg = "[{}][{}] - {}".format(element.data_entrada,aux['function'],aux['msg'])
		except:
			element.msg = "[{}] - {}".format(element.data_entrada,element.msg)
		StreamHandler.emit(self,record=element)

	def write(self,msg):
		print(msg)

	def sendObjects(self):
		for i in session.query(StreamLogStructure).all():
			try:
				self.sendToStream(i)
				session.delete(i)
			except Exception as e:
				print(str(e))
			session.commit()

	def emit(self, record):
		time = datetime.datetime.now()
		if self.save:
			log = StreamLogStructure()
			log.data_entrada = time
			log.levelname = record.levelname
			log.name = record.name
			log.pathname = record.pathname
			log.lineno = record.lineno
			log.msg = record.msg
			log.exc_text = record.exc_text
			log.stack_info = record.stack_info
			log.args = ''
			for i in record.args:
				log.args+=(i+',')
			log.exc_info = record.exc_info
			session.add(log)
			session.commit()
			self.sendObjects()
		else:
			log = StreamLog(
				data_entrada = time,
				levelname = record.levelname,
				name = record.name,
				pathname = record.pathname,
				lineno = record.lineno,
				msg = record.msg,
				exc_text = record.exc_text,
				stack_info = record.stack_info,
				args = '',
				exc_info = record.exc_info
			)
			for arg in record.args:
				log.args+=(arg+',')
			
			self.sendToStream(element=log)