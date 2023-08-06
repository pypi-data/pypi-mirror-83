from logging import StreamHandler
from requests_aws4auth import AWS4Auth
from handlers.es_handler.models import *
from elasticsearch import Elasticsearch,RequestsHttpConnection
import datetime
import ast
import pytz
from collections import namedtuple


class ElasticHandler(StreamHandler):
	def elasticConnection(self):
		self.es = Elasticsearch(hosts=[self.hosts],
					http_auth=AWS4Auth(self.aws_access_key,self.aws_secret_key, self.aws_region,'es'),
					use_ssl=True,
					verify_certs=True,
					connection_class=RequestsHttpConnection)
		self.es.indices.create(index=self.index, ignore=400)

	def __init__(self, hosts,aws_access_key,aws_secret_key,aws_region,index,save=True):
		StreamHandler.__init__(self)
		connected = False
		self.hosts = hosts
		self.aws_access_key = aws_access_key
		self.aws_secret_key = aws_secret_key
		self.aws_region = aws_region
		self.index = index

		while not connected:
			try:
				self.elasticConnection()
				connected = True
			except:
				connected = False
		self.save = save
		if self.save:
			metadata.create_all(engine)

	def sendToElastic(self,element):
		try:
			aux = ast.literal_eval(element.msg)
		except:
			aux = dict()
			aux['msg'] = element.msg
		aux['data_entrada'] = element.data_entrada
		aux['levelname'] = element.levelname
		aux['name'] = element.name
		aux['pathname'] = element.pathname
		aux['lineno'] = element.lineno
		aux['args'] = element.args
		aux['exc_info'] = element.exc_info
		self.es.index(index=self.index, body=aux)

	def sendObjects(self):
		try:
			for i in session.query(ElasticLogStructure).all():
				self.sendToElastic(i)
				session.delete(i)
				session.commit()
		except:
			self.elasticConnection()

	def emit(self, record):
		time = datetime.datetime.now()
		if self.save :
			log = ElasticLogStructure()
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
			log = ElasticLog(
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

			self.sendToElastic(element=log)