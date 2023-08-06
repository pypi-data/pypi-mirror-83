import configparser
import logging
from logging.handlers import RotatingFileHandler
from handlers.es_handler import *
from handlers.rocket_handler import *
from handlers.rotating_file_handler import *
from handlers.stream_handler import *
import json
import sys

class Log:
	def __init__(self,confi_name,log_name,log_level='debug',save=True):
		self.logger = logging.getLogger(log_name)
		self.logger.setLevel(self.__get_level(log_level))
		config = configparser.ConfigParser()
		config.read(confi_name)
		for element in config['Handlers'].keys():
			self.logger.addHandler(
				self.__create_handler(
					confi_dict=config[element],
					handler_type=config['Handlers'][element],
					save=save
				)
			)

	def __get_level(self,level):
		try:
			func = {
				'info':logging.INFO,
				'debug':logging.DEBUG,
				'warning':logging.WARNING,
				'error':logging.ERROR,
				'critical':logging.CRITICAL
			}
			return func[level]
		except:
			raise Exception("The logger level must be one of the followings ('info','debug','warning','error','critical')")

	def __create_handler(self,confi_dict,handler_type,save=True):
		try:
			func = {
				'elastic':self.__create_elastic_handler,
				'rocket':self.__create_rocket_handler,
				'rotating':self.__create_rotating_handler,
				'stream':self.__create_stream_handler
			}
		except:
			raise Exception("The handler must belong to one of the following options ('elastic','rocket','rotating','stream')")
		return func[handler_type](confi_dict=confi_dict,save=save)

	def __create_elastic_handler(self,confi_dict,save=True):
		element = ElasticHandler(hosts=confi_dict['host'],
		                      aws_access_key=confi_dict['access_key'],
		                      aws_secret_key=confi_dict['secret_key'],
		                      aws_region=confi_dict['region'],
		                      index=confi_dict['index'],
		                      save=save)
		element.setLevel(self.__get_level(confi_dict['level']))
		return element

	def __create_rocket_handler(self,confi_dict,save=True):
		element = RocketHandler(host=confi_dict['host'],
								login=confi_dict['login'],
								password=confi_dict['password'],
								channel=confi_dict['channel'],
								alias=confi_dict['alias'],
								topic=confi_dict['topic'],
								method=confi_dict['method']
		)
		element.setLevel(self.__get_level(confi_dict['level']))
		return element

	def __create_rotating_handler(self,confi_dict,save=True):
		element = RotatingHandler(file=confi_dict['file'],maxBytes=int(confi_dict['max']))
		element.setLevel(self.__get_level(confi_dict['level']))
		return element

	def __create_stream_handler(self,confi_dict,save=True):
		element = ScreenHandler(save=save)
		element.setLevel(self.__get_level(confi_dict['level']))
		return element

	def __time_log(self,time):
		return time.strftime("[%d/%m/%Y - %H:%M:%S]")

	def log(self,msg_dict,level='info'):
		try:
			func_name = sys._getframe(1).f_code.co_name.replace('_',' ')
			msg_dict['function'] = func_name
			msg_dict['horario'] = str(datetime.datetime.now())
			func = {
				'info':self.logger.info,
				'debug':self.logger.debug,
				'warning':self.logger.warning,
				'error':self.logger.error,
				'critical':self.logger.critical
			}
			func[level](json.dumps(msg_dict))
		except:
			raise Exception("The log level must be one of the followings ('info','debug','warning','error','critical')")