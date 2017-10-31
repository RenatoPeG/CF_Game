import pygame
from Modules.Text import *

class Button:
	def __init__(self, text, color, fontFamily, fontSize, backgroundColor, backgroundColorHover, x, y, width, height, display):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		mousePos = pygame.mouse.get_pos()
		if self.x + self.width > mousePos[0] > self.x and self.y + self.height > mousePos[1] > self.y:
			pygame.draw.rect(display, backgroundColorHover, (self.x, self.y, self.width, self.height))
		else:
			pygame.draw.rect(display, backgroundColor, (self.x, self.y, self.width, self.height))

		Text.renderLabel(text, color, fontFamily, fontSize, (self.x + (self.width / 2)), (self.y + (self.height / 2)), '', display)

	def mouseInBonudaries(self):
		mousePos = pygame.mouse.get_pos()
		return (self.x + self.width > mousePos[0] > self.x and self.y + self.height > mousePos[1] > self.y)