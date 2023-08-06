from logging.handlers import RotatingFileHandler
from handlers.rotating_file_handler.models import *
import datetime
import ast
import pytz

class RotatingHandler(RotatingFileHandler):
	def __init__(self,file,maxBytes):
		super().__init__(maxBytes=maxBytes,filename=file)
		metadata.create_all(engine)
		self.file = file
		self.maxBytes = maxBytes

	def sendToRotatingFile(self,element):
		try:
			aux = ast.literal_eval(element.msg)
			element.msg = "[{}][{}] - {}".format(element.data_entrada,aux['function'],aux['msg'])
		except:
			element.msg = "[{}] - {}".format(element.data_entrada,element.msg)
		super().emit(record=element)

	def sendObjects(self):
		for i in session.query(RotatingFileLogStructure).all():
			try:
				self.sendToRotatingFile(i)
				session.delete(i)
			except Exception as e:
				print(str(e))
			session.commit()

	def emit(self, record):
		log = RotatingFileLogStructure()
		time = datetime.datetime.now()
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