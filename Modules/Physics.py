import pygame
import sys
from Modules.Music import *
from Modules.Option import *
pygame.init()

class Physics():
    # Paths
    charactersSpritesFolder = 'Resources/Sprites/Characters/'
    scenariosSpritesFolder = 'Resources/Sprites/Scenarios/'

    # Constants
    gravity = 10

    def __init__(self, display, currentDisplayWidth, currentDisplayHeight, player1Character, player2Character):
        # Set display parameters
        self.currentDisplayWidth = currentDisplayWidth
        self.currentDisplayHeight = currentDisplayHeight

        # Set the players that will fight
        self.player1 = self.Player(player1Character, pygame.math.Vector2(0, 0), 1)
        self.player2 = self.Player(player2Character, pygame.math.Vector2(1000, 0), -1)

        # Set the scenario
        self.scenario = pygame.image.load(Physics.scenariosSpritesFolder + "scenario.png").convert()

        # Set display
        self.display = display

        # Set clock
        self.clock = pygame.time.Clock()

        # Play music and set volume
        Music.playSong(2)
        Music.setVolume(Option.volume)

    class Collider():
        def __init__(self, width, height, canCollide):
            pass

    class Player():
        def __init__(self, character, initialPosition, lookingDirection):
            self.character = character

            # Initialize vectors
            self.position = initialPosition
            self.velocity = pygame.math.Vector2(0, 0)

            # Player looking direction
            self.lookingDirection = lookingDirection

            # Initialize sprites
            filePrefix = Physics.charactersSpritesFolder + self.character['name'] + "/" + self.character['asset_prefix']
            self.moveSprite = pygame.image.load(filePrefix + "_move.png").convert_alpha()
            self.moveInvSprite = pygame.image.load(filePrefix + "_move.png").convert_alpha()

            if self.lookingDirection == 1:
                self.currentSprite = self.moveSprite
            elif self.lookingDirection == -1:
                self.currentSprite = self.moveInvSprite
            
    def startFight(self):
        while True:
            # Analize events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw the scenario
            self.display.blit(self.scenario, (0, 0))
            self.display.blit(self.player1.currentSprite, self.player1.position)
            self.display.blit(self.player2.currentSprite, self.player2.position)

            # Render all
            pygame.display.flip()

            # Refresh
            pygame.display.update()
            self.clock.tick(60)