import requests

class Proxy():
	baseUrl = 'http://localhost:8000/api-cholofighter/'

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