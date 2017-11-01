import pygame

class Music:
	# Static variables
	musicPath = 'Resources/Music/'
	tracklist = {
		1: 'quiero_amanecer.mp3',
		2: 'el_cervecero.mp3'
	}

	@staticmethod
	def playSong(track):
		filePath = Music.musicPath + Music.tracklist[track]
		try:
			pygame.mixer.music.load(filePath)
			pygame.mixer.music.play(-1, 0.0)
		except pygame.error as message:
			print('Cannot load audio file')
			raise SystemExit(message)

	@staticmethod
	def toggleMusic():
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
			pygame.mixer.music.get_pos()
		else:
			pygame.mixer.music.play()

	@staticmethod
	def setVolume(value):
		pygame.mixer.music.set_volume(value)