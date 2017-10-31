from Modules.Menu import *

class Game:
	def __init__(self):
		pass

	def startGame(self):
		menu = Menu()

		# First window to load
		menu.gameMenu()

if __name__ == '__main__':
	choloFighter = Game()
	choloFighter.startGame()