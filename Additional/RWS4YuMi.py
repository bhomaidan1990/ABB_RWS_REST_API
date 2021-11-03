#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, LIG lab/ Marven Team, France, 2021.
| RWS4YuMi API.
'''
from requests import get, Session
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET

#======================
# class actionHandler |
#======================

class RWS4YuMi():
	def __init__(self, host='http://192.168.125.1', username='Default User', password='robotics'):
		"""
		Class RWS4YuMi: API with ABB YuMI IRB14000 Robot.
		---
		Parameters:
		@param: host, string, root ip address and port 80 for http.
		@param: username, string, username.
		@param: password, string, password.
		"""

		self.host = host
		self.username = username
		self.password = password
		self.session = Session() # create persistent HTTP communication
		self.session.auth = HTTPDigestAuth(self.username, self.password)

	def actionStatus(self):
		"""
		Function: actionStatus, to get the robot status: running/stopped.
		---
		Parameters:
		@param: None
		---
		@return: status, string, running/stopped.
		"""

		url = self.host+"/rw/rapid/execution"

		status = ''
		r = get(url, auth=HTTPDigestAuth(self.username, self.password), verify=False,  stream=True)
		if(r.status_code != 200):
			print("Exit with Request Error Code: ", r.status_code)
			return None

		tree = ET.fromstring(r.content)

		k = {'class': 'ctrlexecstate'}

		for child in tree[1].iter('*'):
			if child.attrib==k:
				status = child.text

		return status

	def getRobtarget(self, mechUnit='ROB_L'):
		"""
		Function: getRobtarget, to get the robot robtarget.
		---
		Parameters:
		@param: mechUnit, string, 'ROB_L' or 'ROB_R'.
		---
		@return: robtarget, list of lists, robtarget.
		"""
		url = self.host+"/rw/motionsystem/mechunits/"+mechUnit+"/robtarget"

		r = get(url, auth=HTTPDigestAuth(self.username, self.password), verify=False,  stream=True)
		if(r.status_code != 200):
			print("Exit with Request Error Code: ", r.status_code)
			return False

		tree = ET.fromstring(r.content)

		for child in tree[1].iter('*'):
			if child.attrib == {'class': 'x'}:
				x = float(child.text)
			elif child.attrib == {'class': 'y'}:
				y = float(child.text)
			elif child.attrib == {'class': 'z'}:
				z = float(child.text)
			elif child.attrib == {'class': 'q1'}:
				q1 = float(child.text)
			elif child.attrib == {'class': 'q2'}:
				q2 = float(child.text)
			elif child.attrib == {'class': 'q3'}:
				q3 = float(child.text)
			elif child.attrib == {'class': 'q4'}:
				q4 = float(child.text)
			elif child.attrib == {'class': 'cf1'}:
				cf11 = float(child.text)
			elif child.attrib == {'class': 'cf4'}:
				cf14 = float(child.text)
			elif child.attrib == {'class': 'cf6'}:
				cf16 = float(child.text)
			elif child.attrib == {'class': 'cfx'}:
				cf1x = float(child.text)
			elif child.attrib == {'class': 'eax_a'}:
				eax_a = float(child.text)

		robtarget = [[x, y, z], [q1, q2, q3, q4], [cf11, cf14, cf16, cf1x], [eax_a, '9E+09', '9E+09', '9E+09', '9E+09', '9E+09']] # eax_b, eax_c, eax_d, eax_e, eax_f]]
		
		return robtarget

	def getJointtarget(self, mechUnit='ROB_L'):
		"""
		Function: getJointtarget, to get the robot robtarget.
		---
		Parameters:
		@param: mechUnit, string, 'ROB_L' or 'ROB_R'.
		---
		@return: jointtarget, list of lists, jointtarget.
		"""
		url = self.host+"/rw/motionsystem/mechunits/"+mechUnit+"/jointtarget"

		r = get(url, auth=HTTPDigestAuth(self.username, self.password), verify=False,  stream=True)
		if(r.status_code != 200):
			print("Exit with Request Error Code: ", r.status_code)
			return False

		tree = ET.fromstring(r.content)

		for child in tree[1].iter('*'):
			if child.attrib == {'class': 'rax_1'}:
				rax_1 = float(child.text)
			elif child.attrib == {'class': 'rax_2'}:
				rax_2 = float(child.text)
			elif child.attrib == {'class': 'rax_3'}:
				rax_3 = float(child.text)
			elif child.attrib == {'class': 'rax_4'}:
				rax_4 = float(child.text)
			elif child.attrib == {'class': 'rax_5'}:
				rax_5 = float(child.text)
			elif child.attrib == {'class': 'rax_6'}:
				rax_6 = float(child.text)
			elif child.attrib == {'class': 'eax_a'}:
				eax_a = float(child.text)

		jointtarget = [[rax_1, rax_2, rax_3, rax_4, rax_5, rax_6], [eax_a, '9E+09', '9E+09', '9E+09', '9E+09', '9E+09']] # eax_b, eax_c, eax_d, eax_e, eax_f]]
		
		return jointtarget
#-------------------------------------------------------------

# api = RWS4YuMi()
# print(api.getRobtarget())