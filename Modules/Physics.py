import math
import pygame
import sys
from Modules.Color import *
from Modules.Music import *
from Modules.Option import *
from Modules.Text import *
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

        # Set display
        self.display = display

        # Set clock
        self.clock = pygame.time.Clock()

        # Set match timer
        self.timer = self.Timer(Option.timeLimit, self.display)
        
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
        self.player1 = self.Player(player1Character, pygame.math.Vector2(100, 0), 1, self.display)
        self.player2 = self.Player(player2Character, pygame.math.Vector2(self.currentDisplayWidth - 200, 0), -1, self.display)

        # Set all the status bars
        self.player1HealthBar = self.Bar(100, Color.red, 50, 50, (Physics.baseDisplayWidth / 2) - 150, 30, 'left', self.display)
        self.player2HealthBar = self.Bar(100, Color.red, Physics.baseDisplayWidth - ((Physics.baseDisplayWidth / 2) - 150) - 50, 50, (Physics.baseDisplayWidth / 2) - 150, 30, 'right', self.display)
        self.player1StaminaBar = self.Bar(0, Color.blue, 50, 85, (Physics.baseDisplayWidth / 2) - 200, 20, 'left', self.display)
        self.player2StaminaBar = self.Bar(0, Color.blue, Physics.baseDisplayWidth - ((Physics.baseDisplayWidth / 2) - 200) - 50, 85, (Physics.baseDisplayWidth / 2) - 200, 20, 'right', self.display)

        # Set players' projectiles
        self.player1Projectile = self.Projectile(player1Character, self.player2, self.display)
        self.player2Projectile = self.Projectile(player2Character, self.player1, self.display)

        # Set the scenario
        self.scenario = pygame.image.load(Physics.scenariosSpritesFolder + 'plaza_mayor.png').convert()

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

    class Bar():
        def __init__(self, startingValue, color, x, y, width, height, align, display):
            self.value = startingValue
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.align = align
            self.display = display

        def increaseValue(self, increment):
            if (self.value + increment > 100):
                self.value = 100
            else:
                self.value = self.value + increment

        def decreaseValue(self, decrement):
            if (self.value - decrement < 0):
                self.value = 0
            else:
                self.value = self.value - decrement

        def render(self):
            filledDistance = math.floor((self.width - 4) * (self.value / 100))
            pygame.draw.rect(self.display, Color.black, (self.x, self.y, self.width, self.height))
            if self.align == 'left':
                pygame.draw.rect(self.display, self.color, (self.x + 2, self.y + 2, filledDistance, self.height - 4))
            elif self.align == 'right':
                pygame.draw.rect(self.display, self.color, (self.x + self.width - filledDistance - 2, self.y + 2, filledDistance, self.height - 4))

    class Timer():
        def __init__(self, startingValue, display):
            self.value = startingValue
            self.remainingTicks = self.value * 3600
            self.display = display

        def tick(self, ticks):
            if (self.remainingTicks - ticks < 0):
                self.remainingTicks = 0
            else:
                self.remainingTicks = self.remainingTicks - ticks
            self.value = math.ceil(self.remainingTicks / 3600)

        def render(self):
            x = Physics.baseDisplayWidth / 2
            y = 40
            width = 80
            height = 80
            pygame.draw.rect(self.display, Color.black, (x - (width / 2), y, width, height))
            Text.renderLabel(str(self.value), 'white', 'dolphins.ttf', 36, x, y + (height / 2), '', self.display)

    class Cooldown():
        def __init__(self, duration):
            self.duration = duration
            self.remainingTicks = 0
            self.isReady = True

        def start(self):
            self.remainingTicks = self.duration * 3600
            self.isReady = False

        def tick(self, ticks):
            if (self.remainingTicks - ticks < 0):
                self.remainingTicks = 0
            else:
                self.remainingTicks = self.remainingTicks - ticks
            if self.remainingTicks == 0:
                self.isReady = True

    class Action():
        def __init__(self, name, duration):
            self.name = name
            self.duration = duration
            self.remainingTicks = 0
            self.done = True

        def start(self):
            self.remainingTicks = self.duration * 3600
            self.done = False

        def tick(self, ticks):
            if (self.remainingTicks - ticks < 0):
                self.remainingTicks = 0
            else:
                self.remainingTicks = self.remainingTicks - ticks
            if self.remainingTicks == 0:
                self.done = True

        def abort(self):
            self.remainingTicks = 0
            self.done = True

    class Projectile():
        # Constants
        speed = 20

        def __init__(self, character, targetPlayer, display):
            self.targetPlayer = targetPlayer
            self.display = display
            self.active = False
            self.position = pygame.math.Vector2(0, 0)
            self.shootingDirection = 1
            self.isCollidingTargetPlayer = False

            # Load the sprite
            filePrefix = Physics.charactersSpritesFolder + character['name'] + "/" + character['asset_prefix']
            self.sprite = pygame.image.load(filePrefix + '_projectile.png').convert_alpha()

            # Get projectile dimentions
            self.width = self.sprite.get_rect().size[0]
            self.height = self.sprite.get_rect().size[1]

        def fire(self, initialPosition, shootingDirection):
            self.position[0] = initialPosition[0]
            self.position[1] = initialPosition[1] - math.floor(self.height / 2)
            self.shootingDirection = shootingDirection
            self.active = True

        def move(self):
            self.position[0] = self.position[0] + (self.shootingDirection * Physics.Projectile.speed)

            xCollision = False
            if (self.position[0] > self.targetPlayer.collider.position[0]):
                if ((self.targetPlayer.collider.position[0] + self.targetPlayer.collider.width) < self.position[0]):
                    xCollision = True
            elif (self.targetPlayer.collider.position[0] > self.position[0]):
                if ((self.position[0] + self.width) < self.targetPlayer.collider.position[0]):
                    xCollision = True

            yCollision = False
            if (self.position[1] > self.targetPlayer.collider.position[1]):
                if ((self.targetPlayer.collider.position[1] + self.targetPlayer.collider.height) < self.position[1]):
                    yCollision = True
            elif (self.targetPlayer.collider.position[1] > self.position[1]):
                if ((self.position[1] + self.height) < self.targetPlayer.collider.position[1]):
                    yCollision = True

            self.isCollidingTargetPlayer = xCollision and yCollision

            if ((self.position[0] + self.width) < 0 or self.position[0] > Physics.baseDisplayWidth):
                self.active = False
            
        def render(self):
            self.display.blit(self.sprite, self.position)

    class Beam():
        def __init__(self):
            pass

        def abort(self):
            pass
            
    class Player():
        def __init__(self, character, initialPosition, lookingDirection, display):
            self.character = character
            self.display = display

            # Player state (by default it's Move; other states are: Attack, Damage, Death)
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

            # Initialize cooldowns
            self.primaryBasicAttackCooldown = Physics.Cooldown(0.5)
            self.secondaryBasicAttackCooldown = Physics.Cooldown(0.5)
            self.basicPowerCooldown = Physics.Cooldown(2)
            self.specialPowerCooldown = Physics.Cooldown(0)

            # Initialize actions
            self.primaryBasicAttackAction = Physics.Action('primaryBasicAttack', 0.25)
            self.secondaryBasicAttackAction = Phtsics.Action('secondaryBasicAttack', 0.25)
            self.basicPowerAction = Physics.Action('basicPower', 0.25)
            self.specialPowerAction = Physics.Action('specialPower', 1)

            self.playerCurrentAction = None

            # Player looking direction
            self.lookingDirection = lookingDirection

            if self.lookingDirection == 1:
                self.currentSprite = self.moveSprite
            elif self.lookingDirection == -1:
                self.currentSprite = self.moveSpriteInv

        def render(self):
            self.display.blit(self.currentSprite, self.collider.position)
            
    def startFight(self):
        while True:
            # Analize events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Analyze keys
            keysPressed = pygame.key.get_pressed()

            if self.player1.state == 'Move':
                # Move
                if keysPressed[Option.controlPlayer1.moveLeft] or keysPressed[Option.controlPlayer1.moveRight]:
                    if keysPressed[Option.controlPlayer1.moveLeft]:
                        self.player1.collider.velocity[0] = -Physics.playerMovementSpeed
                    elif keysPressed[Option.controlPlayer1.moveRight]:
                        self.player1.collider.velocity[0] = Physics.playerMovementSpeed
                else:
                    self.player1.collider.velocity[0] = 0
                # Jump
                if keysPressed[Option.controlPlayer1.jump]:
                    if self.player1.collider.isFloored:
                        self.player1.collider.velocity[1] = -30
                # Basic power
                player1StartBasicPower = True
                for key in Option.controlPlayer1.basicPower:
                    if not keysPressed[key]:
                        player1StartBasicPower = False
                        
            if self.player2.state == 'Move':
                # Move
                if keysPressed[Option.controlPlayer2.moveLeft] or keysPressed[Option.controlPlayer2.moveRight]:
                    if keysPressed[Option.controlPlayer2.moveLeft]:
                        self.player2.collider.velocity[0] = -Physics.playerMovementSpeed
                    elif keysPressed[Option.controlPlayer2.moveRight]:
                        self.player2.collider.velocity[0] = Physics.playerMovementSpeed
                else:
                    self.player2.collider.velocity[0] = 0
                # Jump
                if keysPressed[Option.controlPlayer2.jump]:
                    if self.player2.collider.isFloored:
                        self.player2.collider.velocity[1] = -30
                # Basic power
                player2StartBasicPower = True
                for key in Option.controlPlayer2.basicPower:
                    if not keysPressed[key]:
                        player2StartBasicPower = False

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

            # Start attacks
            if player1StartBasicPower and not self.player1Projectile.active and self.player1.basicPowerCooldown.isReady and self.player1.collider.isFloored:
                player1ProjectileInitialPositionX = self.player1.collider.position[0] + (self.player1.collider.width / 2)
                player1ProjectileInitialPositionY = self.player1.collider.position[1] + (self.player1.collider.height / 2)
                player1ProjectileInitialPositionVector = pygame.math.Vector2(player1ProjectileInitialPositionX, player1ProjectileInitialPositionY)
                self.player1Projectile.fire(player1ProjectileInitialPositionVector, self.player1.lookingDirection)
                self.player1.basicPowerCooldown.start()
            if player2StartBasicPower and not self.player2Projectile.active and self.player2.basicPowerCooldown.isReady and self.player2.collider.isFloored:
                player2ProjectileInitialPositionX = self.player2.collider.position[0] + (self.player2.collider.width / 2)
                player2ProjectileInitialPositionY = self.player2.collider.position[1] + (self.player2.collider.height / 2)
                player2ProjectileInitialPositionVector = pygame.math.Vector2(player2ProjectileInitialPositionX, player2ProjectileInitialPositionY)
                self.player2Projectile.fire(player2ProjectileInitialPositionVector, self.player2.lookingDirection)
                self.player2.basicPowerCooldown.start()

            # Update colliders
            self.player1.collider.move()
            self.player2.collider.move()

            # Update projectiles
            if self.player1Projectile.active:
                self.player1Projectile.move()
            if self.player2Projectile.active:
                self.player2Projectile.move()
                
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

            # Update timer
            self.timer.tick(60)

            # Update cooldowns
            self.player1.primaryBasicAttackCooldown.tick(60)
            self.player1.basicPowerCooldown.tick(60)
            self.player2.primaryBasicAttackCooldown.tick(60)
            self.player2.basicPowerCooldown.tick(60)

            # Draw the scenario
            self.display.blit(self.scenario, (0, 0))
            self.player1HealthBar.render()
            self.player2HealthBar.render()
            self.player1StaminaBar.render()
            self.player2StaminaBar.render()
            self.timer.render()

            # Render the players
            self.player1.render()
            self.player2.render()

            # Render the projectiles
            if self.player1Projectile.active:
                self.player1Projectile.render()
            if self.player2Projectile.active:
                self.player2Projectile.render()

            # Render all
            pygame.display.flip()

            # Refresh
            pygame.display.update()
            self.clock.tick(60)