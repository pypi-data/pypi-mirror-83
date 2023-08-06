from logging import StreamHandler
from requests_aws4auth import AWS4Auth
from handlers.rocket_handler.rocketbot import *
from handlers.rocket_handler.models import *
import datetime
import ast
import pytz

class RocketHandler(StreamHandler):
	def rocketConnection(self):
		self.bot = Rocketbot(endpoint=self.host,
							username=self.login,
							password=self.password)

	def __init__(self, host,login,password,channel,alias,topic,email=None,method='normal'):
		StreamHandler.__init__(self)
		metadata.create_all(engine)
		connected = False
		self.host = host
		self.login = login
		self.password = password
		self.channel = channel
		self.alias = alias
		self.method = method
		self.topic = topic
		self.email = email
		while not connected:
			try:
				self.rocketConnection()
				connected = True
			except Exception as e:
				connected = False

	def __dict_to_text(self,msg_dict):
		msg_string = str()
		try:
			msg_string += '*'+msg_dict['topic']+'*\n'
			if 'subtopic' in msg_dict.keys():
				for element in msg_dict['subtopic'].keys():
					msg_string += '    -{} : {}\n'.format(element,msg_dict['subtopic'][element])
			if 'msg' in msg_dict.keys():
				try:
					for element in msg_dict['msg'].keys():
						msg_string+= '\n```\n'
						msg_string+= '    -{}'.format(msg_dict['msg'][element])
						msg_string+= '\n```\n'
				except:
					msg_string=str()
					msg_string+= '\n```\n'
					msg_string+= '    -{}'.format(msg_dict['msg'])
					msg_string+= '\n```\n'
			return msg_string
		except:
			return None

	def sendToRocket(self,element):
		try:
			aux = ast.literal_eval(element.msg)
			text = self.__dict_to_text(aux)
			if text == None:
				raise Exception('Empty message')
		except:
			text = element.msg

		if element.method == 'normal':
			self.bot.post_message(channel = element.channel,text=text,alias=element.alias,emoji=':robot:')
		elif element.method == 'livechat':
			self.bot.send_livechat_message(name=element.alias,
										   email=self.email,
										   msg=text,
										   topico=element.topic,
										   department=element.msg)
		else:	
			raise Exception('Chat method Error')


	def sendObjects(self):
		for i in session.query(RocketLogStructure).all():
			try:
				self.sendToRocket(i)
				session.delete(i)
			except Exception as e:
				print(str(e))
			session.commit()

	def emit(self, record):
		log = RocketLogStructure()
		time = datetime.datetime.now()
		log.data_entrada = time
		log.levelname = record.levelname
		log.name = record.name
		log.pathname = record.pathname
		log.lineno = record.lineno
		log.alias = self.alias
		log.channel = self.channel
		log.method = self.method
		log.topic = self.topic
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