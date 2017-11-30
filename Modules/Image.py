#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

class Image:
	# Static variables
	imagePath = 'Resources/Images/'

	def loadImage(fileName):
		filePath = Image.imagePath + fileName
		try:
			image = pygame.image.load(filePath)
			image = image.convert()
			return image, image.get_rect()
		except pygame.error as message:
			print('Cannot load image: %s' % fileName)
			raise SystemExit(message)   
