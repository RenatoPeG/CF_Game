#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

class Proxy():
	baseUrl = 'http://52.226.131.0/api-cholofighter/v1/'

	@staticmethod
	def getCharacters():
		url = Proxy.baseUrl + "character/"
		return requests.get(url).json()

	@staticmethod
	def getScenarios():
		url = Proxy.baseUrl + "scenario/"
		return requests.get(url).json()

	@staticmethod
	def getScores():
		url = Proxy.baseUrl + "score/"
		return requests.get(url).json()

	@staticmethod
	def setScore(name, score):
		url = Proxy.baseUrl + "score/"
		payload = {'name': name, 'score': score}
		return requests.post(url, data=payload)