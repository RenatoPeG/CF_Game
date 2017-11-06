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
    gravity = 2
    floorElevation = 50
    playerMovementSpeed = 6

    baseDisplayWidth = 1200
    baseDisplayHeight = 700

    def __init__(self, display, currentDisplayWidth, currentDisplayHeight, player1Character, player2Character):
        # Set display parameters
        self.currentDisplayWidth = currentDisplayWidth
        self.currentDisplayHeight = currentDisplayHeight

        # Set global scale
        self.globalScale = 1

        widthExpansion = self.currentDisplayWidth / Physics.baseDisplayWidth
        heightExpansion = self.currentDisplayHeight / Physics.baseDisplayHeight

        if self.currentDisplayWidth > Physics.baseDisplayWidth:
            if (widthExpansion * Physics.baseDisplayHeight) > self.currentDisplayHeight:
                self.globalScale = heightExpansion
            else:
                self.globalScale = widthExpansion
        elif self.currentDisplayHeight > Physics.baseDisplayHeight:
            if (heightExpansion * Physics.baseDisplayWidth) > self.currentDisplayWidth:
                self.globalScale = widthExpansion
            else:
                self.globalScale = heightExpansion

        # Set the players that will fight
        self.player1 = self.Player(player1Character, pygame.math.Vector2(100, 0), 1)
        self.player2 = self.Player(player2Character, pygame.math.Vector2(self.currentDisplayWidth - 200, 0), -1)

        # Set the scenario
        self.scenario = pygame.image.load(Physics.scenariosSpritesFolder + 'plaza_mayor.png').convert()

        # Set display
        self.display = display

        # Set clock
        self.clock = pygame.time.Clock()

        # Play music and set volume
        Music.playSong(2)
        Music.setVolume(Option.volume)

    class Collider():
        def __init__(self, width, height, initialPosition):
            self.width = width
            self.height = height
            self.position = initialPosition
            self.velocity = pygame.math.Vector2(0, 0)
            self.isFloored = False

        def move(self):
            # Apply gravity
            self.velocity[1] = self.velocity[1] + Physics.gravity

            # Analize if...
            # ...touching roof
            if (self.position[1] < 0):
                self.position[1] = 0
                if (self.velocity[1] < 0):
                    self.velocity[1] = 0
            # ...touching floor
            if (self.position[1] + self.height >= Physics.baseDisplayHeight - Physics.floorElevation):
                self.position[1] = Physics.baseDisplayHeight - Physics.floorElevation - self.height
                self.isFloored = True
                if (self.velocity[1] > 0):
                    self.velocity[1] = 0
            else:
                self.isFloored = False
            # ...touching left limit
            if (self.position[0] < 0):
                self.position[0] = 0
                if (self.velocity[0] < 0):
                    self.velocity[0] = 0
            # ...touching right limit
            if (self.position[0] + self.width > Physics.baseDisplayWidth):
                self.position[0] = Physics.baseDisplayWidth - self.width
                if (self.velocity[0] > 0):
                    self.velocity[0] = 0

            # Update position
            self.position = self.position + self.velocity

    class Player():
        def __init__(self, character, initialPosition, lookingDirection):
            self.character = character

            # Player state (by default it's Move, other states are: Attack, Damage, Death)
            self.state = 'Move'

            # Initialize sprites
            filePrefix = Physics.charactersSpritesFolder + self.character['name'] + "/" + self.character['asset_prefix']
            self.moveSprite = pygame.image.load(filePrefix + '_move.png').convert_alpha()
            self.moveSpriteInv = pygame.image.load(filePrefix + '_move_inv.png').convert_alpha()
            self.jumpSprite = pygame.image.load(filePrefix + '_jump.png').convert_alpha()
            self.jumpSpriteInv = pygame.image.load(filePrefix + '_jump_inv.png').convert_alpha()
            self.primaryBasicAttackSprite = pygame.image.load(filePrefix + '_primary_basic_attack.png').convert_alpha()
            self.primaryBasicAttackSpriteInv = pygame.image.load(filePrefix + '_primary_basic_attack_inv.png').convert_alpha()

            # Initialize collider
            self.collider = Physics.Collider(self.moveSprite.get_rect().size[0], self.moveSprite.get_rect().size[1], initialPosition)

            # Player looking direction
            self.lookingDirection = lookingDirection

            if self.lookingDirection == 1:
                self.currentSprite = self.moveSprite
            elif self.lookingDirection == -1:
                self.currentSprite = self.moveSpriteInv
            
    def startFight(self):
        while True:
            # Analize events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Analyse keys
            keysPressed = pygame.key.get_pressed()

            if self.player1.state == 'Move':
                if keysPressed[Option.controlPlayer1.moveLeft] or keysPressed[Option.controlPlayer1.moveRight]:
                    if keysPressed[Option.controlPlayer1.moveLeft]:
                        self.player1.collider.velocity[0] = -Physics.playerMovementSpeed
                    elif keysPressed[Option.controlPlayer1.moveRight]:
                        self.player1.collider.velocity[0] = Physics.playerMovementSpeed
                else:
                    self.player1.collider.velocity[0] = 0
                if keysPressed[Option.controlPlayer1.jump]:
                    if self.player1.collider.isFloored:
                        self.player1.collider.velocity[1] = -30
                if keysPressed[Option.controlPlayer1.primaryBasicAttack]:
                    pass

            if self.player2.state == 'Move':
                if keysPressed[Option.controlPlayer2.moveLeft] or keysPressed[Option.controlPlayer2.moveRight]:
                    if keysPressed[Option.controlPlayer2.moveLeft]:
                        self.player2.collider.velocity[0] = -Physics.playerMovementSpeed
                    elif keysPressed[Option.controlPlayer2.moveRight]:
                        self.player2.collider.velocity[0] = Physics.playerMovementSpeed
                else:
                    self.player2.collider.velocity[0] = 0
                if keysPressed[Option.controlPlayer2.jump]:
                    if self.player2.collider.isFloored:
                        self.player2.collider.velocity[1] = -30

            # Update looking direction
            if self.player1.collider.isFloored:
                if self.player1.collider.velocity[0] > 0:
                    self.player1.lookingDirection = 1
                elif self.player1.collider.velocity[0] < 0:
                    self.player1.lookingDirection = -1

            if self.player2.collider.isFloored:
                if self.player2.collider.velocity[0] > 0:
                    self.player2.lookingDirection = 1
                elif self.player2.collider.velocity[0] < 0:
                    self.player2.lookingDirection = -1

            # Update colliders
            self.player1.collider.move()
            self.player2.collider.move()

            # Update sprites
            if self.player1.state == 'Move':
                if self.player1.collider.isFloored:
                    if self.player1.lookingDirection == 1:
                        self.player1.currentSprite = self.player1.moveSprite
                    elif self.player1.lookingDirection == -1:
                        self.player1.currentSprite = self.player1.moveSpriteInv
                else:
                    if self.player1.lookingDirection == 1:
                        self.player1.currentSprite = self.player1.jumpSprite
                    elif self.player1.lookingDirection == -1:
                        self.player1.currentSprite = self.player1.jumpSpriteInv

            if self.player2.state == 'Move':
                if self.player2.collider.isFloored:
                    if self.player2.lookingDirection == 1:
                        self.player2.currentSprite = self.player2.moveSprite
                    elif self.player2.lookingDirection == -1:
                        self.player2.currentSprite = self.player2.moveSpriteInv
                else:
                    if self.player2.lookingDirection == 1:
                        self.player2.currentSprite = self.player2.jumpSprite
                    elif self.player2.lookingDirection == -1:
                        self.player2.currentSprite = self.player2.jumpSpriteInv

            # Draw the scenariod
            self.display.blit(self.scenario, (0, 0))
            self.display.blit(self.player1.currentSprite, self.player1.collider.position)
            self.display.blit(self.player2.currentSprite, self.player2.collider.position)

            # Render all
            pygame.display.flip()

            # Refresh
            pygame.display.update()
            self.clock.tick(60)