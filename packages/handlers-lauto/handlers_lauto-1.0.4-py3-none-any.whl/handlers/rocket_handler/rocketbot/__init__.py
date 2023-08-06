import requests
import json
import hashlib
class Rocketbot:
	def __init__(self,endpoint,username,password):
		self.endpoint = endpoint
		self.username = username
		self.password = password
		self.__auth__()

	def __auth__(self):
		payload = 'user={}&password={}'.format(self.username,self.password)
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		updated = False
		while not updated:
			response = requests.post(self.endpoint+'/api/v1/login', headers=headers, data = payload)
			updated = True if response.json()['status'] == 'success' else False
		data = response.json()['data']
		self.userID = data['userId']
		self.token = data['authToken']
		self.emails = list()
		for email in data['me']['emails']:
			self.emails.append({
				'addr':email['address'],
				'verified':email['verified']
			})
		self.name = data['me']['name']

	def __checksum_list(self,ck_list):
		hash_el = hashlib.md5()
		for ck_el in ck_list:
			hash_el.update(ck_el)
		return hash_el.hexdigest()

	def post_message(self,text,alias=None,emoji=None,avatar=None,attachments=None,roomID = None,channel = None):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		data = dict()
		data['channel'] = channel
		data['text'] = text
		if roomID is not None:
			data['roomId'] = roomID
		if alias is not None:
			data['alias'] = alias
		if emoji is not None:
			data['emoji'] = emoji
		if avatar is not None:
			data['avatar'] = avatar
		if attachments is not None:
			data['attachments'] = attachments
		response = requests.post(self.endpoint+'/api/v1/chat.postMessage',headers=headers,data=data)
		return response

	def get_rooms(self):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}

		response = requests.get(self.endpoint+'/api/v1/rooms.get', headers=headers)
		resposta = response.json()
		assert resposta['success']
		grupos = resposta['update']
		return resposta

	def get_room_users(self,room_id):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		params = {
			'roomId':room_id
		}
		response = requests.get(self.endpoint+'/api/v1/groups.members',params=params,headers=headers)
		return response


	def post_offlinelivechat_message(self,msg,email,name):
		data = {
			"name": name,
			"email": email,
			"message": msg
		}
		response = requests.post(self.endpoint+'/api/v1/livechat/offline.message',json=data)
		return response

	def post_livechat_message(self,token,room_id,msg,msg_id=None,room_agent=None):
		data = {
			"token": token,
			"rid": room_id,
			"msg": msg
		}
		if msg_id != None:
			data['_id'] = msg_id
		if room_agent != None:
			data['agent'] = room_agent
		response = requests.post(self.endpoint+'/api/v1/livechat/message',json=data)
		return response
	
	def get_livechat_users(self,type='agent'):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		response = requests.get(self.endpoint+'/api/v1/livechat/users/{}'.format(type), headers=headers)
		return response

	def get_livechat_inquiries(self):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		response = requests.get(self.endpoint+'/api/v1/livechat/inquiries.list', headers=headers)
		return response

	def get_livechat_departments(self):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		response = requests.get(self.endpoint+'/api/v1/livechat/department', headers=headers)
		return response

	def livechat_rooms(self,user_name,room_name=None):
		params = {
			'token':user_name
		}
		url = self.endpoint+'/api/v1/livechat/room'
		if room_name is not None:
			params['rid'] = room_name
		response = requests.get(url,params=params)
		return response

	def get_livechat_rooms(self,open=False):
		params = {}
		params['open'] = open
		url = self.endpoint+'/api/v1/livechat/rooms'
		response = requests.get(url,params=params)
		return response

	def create_livechat_department(self,email,name,description,agents = None):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		data = {
				"department": {
				"enabled": True,
				"showOnRegistration": True,
				"email": email,
				"showOnRegistration": True,
				"name": name,
				"description": description,
				"showOnOfflineForm":True
			},
			"agents":[]
		}
		if agents != None:
			for agent in agents:
				data['agents'].append(agent)

		response = requests.post(self.endpoint+'/api/v1/livechat/department',json=data,headers=headers)
		return response

	def set_livechat(self,email):
		agents = list()
		for user in self.get_livechat_users().json()['users']:
			agents.append(dict(
				agentId = user['_id'],
				username = user['username'],
				count=0,
				order=0
			))
		dep = self.create_livechat_department(email=email,
						                      name='General',
							                  description='General Livechat',
							                  agents=agents
							                 )
		return dep

	def get_livechat_visitor(self,name):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		token = self.__checksum_list([name.replace(' ','').lower().encode('utf-8')])
		response = requests.get(self.endpoint+'/api/v1/livechat/visitor/{}'.\
			format(token),headers=headers)
		return response

	def send_livechat_message(self,name,email,msg,topico,department=None):
		search_visitor = self.get_livechat_visitor(name).json()
		if 'visitor' in search_visitor.keys():
			user = search_visitor
		else:
			user = self.create_livechat_visitor(name=name,email=email).json()
		room = self.livechat_rooms(user_name=self.__checksum_list([name.replace(' ','').lower().encode('utf-8')]),
			                       room_name=self.__checksum_list([name.replace(' ','').lower().encode('utf-8'),
	                       								   topico.replace(' ','').lower().encode('utf-8')])).json()
		if department is None:
			department = 'General'
		departments = self.get_livechat_departments().json()
		_id = None
		for dep in departments['departments']:
			if dep['name'] == department:
				_id = dep['_id']
				break
		if _id is None:
			dep = self.set_livechat().json()
			_id = dep['department']['_id']
		self.transfer_livechat_room(token=user['visitor']['token'],
									room_id=room['room']['_id'],
									department=_id)
		return self.post_livechat_message(token=user['visitor']['token'],
						room_id=room['room']['_id'],
						msg=msg)

	def transfer_livechat_room(self,token,room_id,department):
		data={
			"rid":room_id,
			"token":token,
			"department":department,
		}
		response = requests.post(self.endpoint+'/api/v1/livechat/room.transfer',json=data)
		return response

	def create_livechat_visitor(self,name,email=None,phone=None):
		data = {
		  "visitor": {
		    "name": name,
		    "token":self.__checksum_list([name.replace(' ','').lower().encode('utf-8')]),
		  }
		}
		if email != None:
			data['visitor']['email'] = email
		if phone != None:
			data['visitor']['phone'] = phone
		response = requests.post(self.endpoint+'/api/v1/livechat/visitor',json=data)
		return response

	def get_livechat_departments(self):
		headers = {
			'X-User-Id': self.userID,
			'X-Auth-Token': self.token
		}
		response = requests.get(self.endpoint+'/api/v1/livechat/department',headers=headers)
		return response
