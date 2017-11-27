import math
import pygame
import random
import sys
from Modules.Button import *
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
    playerStumbleSpeed = 2

    def __init__(self, display, currentDisplayWidth, currentDisplayHeight, player1Character, player2Character, scenario):
        # Set display parameters
        self.currentDisplayWidth = currentDisplayWidth
        self.currentDisplayHeight = currentDisplayHeight

        # Set player characters
        self.player1Character = player1Character
        self.player2Character = player2Character

        # Set display
        self.display = display

        # Set clock
        self.clock = pygame.time.Clock()

        # Set the scenario
        self.scenario = pygame.image.load(Physics.scenariosSpritesFolder + scenario + '.png').convert()

        # Play music and set volume
        Music.playSong(2)
        Music.setVolume(Option.volume)

    class Collider():
        def __init__(self, width, height, initialPosition, currentDisplayWidth, currentDisplayHeight):
            self.width = width
            self.height = height
            self.position = initialPosition
            self.currentDisplayWidth = currentDisplayWidth
            self.currentDisplayHeight = currentDisplayHeight
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
            if (self.position[1] + self.height >= self.currentDisplayHeight - Physics.floorElevation):
                self.position[1] = self.currentDisplayHeight - Physics.floorElevation - self.height
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
            if (self.position[0] + self.width > self.currentDisplayWidth):
                self.position[0] = self.currentDisplayWidth - self.width
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
        def __init__(self, startingValue, currentDisplayWidth, display):
            self.value = startingValue
            self.remainingTicks = self.value * 3600
            self.currentDisplayWidth = currentDisplayWidth
            self.display = display

        def tick(self, ticks):
            if (self.remainingTicks - ticks < 0):
                self.remainingTicks = 0
            else:
                self.remainingTicks = self.remainingTicks - ticks
            self.value = math.ceil(self.remainingTicks / 3600)

        def render(self):
            x = self.currentDisplayWidth / 2
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
        def __init__(self, sprite, spriteInv, duration):
            self.sprite = sprite
            self.spriteInv = spriteInv
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
        damage = 20

        def __init__(self, character, currentDisplayWidth, display):
            self.currentDisplayWidth = currentDisplayWidth
            self.display = display
            self.active = False
            self.position = pygame.math.Vector2(0, 0)
            self.shootingDirection = 1
            self.isCollidingTargetPlayer = False

            # Load the sprite
            filePrefix = Physics.charactersSpritesFolder + character['name'] + "/" + character['asset_prefix']
            self.projectileSprite = pygame.image.load(filePrefix + '_projectile.png').convert_alpha()
            self.projectileSpriteInv = pygame.image.load(filePrefix + '_projectile_inv.png').convert_alpha()
            self.sprite = self.projectileSprite

            # Get projectile dimentions
            self.width = self.sprite.get_rect().size[0]
            self.height = self.sprite.get_rect().size[1]

        def fire(self, initialPosition, shootingDirection):
            self.position[0] = initialPosition[0]
            self.position[1] = initialPosition[1] - math.floor(self.height / 2)
            self.shootingDirection = shootingDirection
            if self.shootingDirection == 1:
                self.sprite = self.projectileSprite
            elif self.shootingDirection == -1:
                self.sprite = self.projectileSpriteInv
            self.active = True

        def move(self, targetPlayer):
            self.position[0] = self.position[0] + (self.shootingDirection * Physics.Projectile.speed)

            xCollision = False
            if (self.position[0] > targetPlayer.collider.position[0]):
                if ((targetPlayer.collider.position[0] + targetPlayer.collider.width) > self.position[0]):
                    xCollision = True
            elif (targetPlayer.collider.position[0] > self.position[0]):
                if ((self.position[0] + self.width) > targetPlayer.collider.position[0]):
                    xCollision = True

            yCollision = False
            if (self.position[1] > targetPlayer.collider.position[1]):
                if ((targetPlayer.collider.position[1] + targetPlayer.collider.height) > self.position[1]):
                    yCollision = True
            elif (targetPlayer.collider.position[1] > self.position[1]):
                if ((self.position[1] + self.height) > targetPlayer.collider.position[1]):
                    yCollision = True

            self.isCollidingTargetPlayer = xCollision and yCollision

            if ((self.position[0] + self.width) < 0 or self.position[0] > self.currentDisplayWidth):
                self.active = False
            
        def render(self):
            self.display.blit(self.sprite, self.position)

    class Beam():
        def __init__(self):
            pass

        def abort(self):
            pass

    class DamageInstance():
        def __init__(self, width, height, damage):
            self.width = width
            self.height = height
            self.damage = damage
            
        def trigger(self, x, y, targetPlayer):
            xCollision = False
            if (x > targetPlayer.collider.position[0]):
                if ((targetPlayer.collider.position[0] + targetPlayer.collider.width) > x):
                    xCollision = True
            elif (targetPlayer.collider.position[0] > x):
                if ((x + self.width) > targetPlayer.collider.position[0]):
                    xCollision = True
            
            yCollision = False
            if (y > targetPlayer.collider.position[1]):
                if ((targetPlayer.collider.position[1] + targetPlayer.collider.height) > y):
                    yCollision = True
            elif (targetPlayer.collider.position[1] > y):
                if ((y + self.height) > targetPlayer.collider.position[1]):
                    yCollision = True
            
            return xCollision and yCollision
            
    class Player():
        def __init__(self, character, initialPosition, lookingDirection, currentDisplayWidth, currentDisplayHeight, display):
            self.character = character
            self.display = display

            # Player state (by default it's Move; other states are: Attack, Damage, Death)
            self.state = 'Move'

            # Initialize bars
            self.healthBar = None
            self.staminaBar = None

            # Initialize sprites
            filePrefix = Physics.charactersSpritesFolder + self.character['name'] + "/" + self.character['asset_prefix']
            self.moveSprite = pygame.image.load(filePrefix + '_move.png').convert_alpha()
            self.moveSpriteInv = pygame.image.load(filePrefix + '_move_inv.png').convert_alpha()
            self.jumpSprite = pygame.image.load(filePrefix + '_jump.png').convert_alpha()
            self.jumpSpriteInv = pygame.image.load(filePrefix + '_jump_inv.png').convert_alpha()
            self.primaryBasicAttackSprite = pygame.image.load(filePrefix + '_primary_basic_attack.png').convert_alpha()
            self.primaryBasicAttackSpriteInv = pygame.image.load(filePrefix + '_primary_basic_attack_inv.png').convert_alpha()
            self.secondaryBasicAttackSprite = pygame.image.load(filePrefix + '_secondary_basic_attack.png').convert_alpha()
            self.secondaryBasicAttackSpriteInv = pygame.image.load(filePrefix + '_secondary_basic_attack_inv.png').convert_alpha()
            self.basicPowerSprite = pygame.image.load(filePrefix + '_basic_power.png').convert_alpha()
            self.basicPowerSpriteInv = pygame.image.load(filePrefix + '_basic_power_inv.png').convert_alpha()
            self.specialPowerSprite = pygame.image.load(filePrefix + '_special_power.png').convert_alpha()
            self.specialPowerSpriteInv = pygame.image.load(filePrefix + '_special_power_inv.png').convert_alpha()
            self.painSprite = pygame.image.load(filePrefix + '_pain.png').convert_alpha()
            self.painSpriteInv = pygame.image.load(filePrefix + '_pain_inv.png').convert_alpha()
            self.deathSprite = pygame.image.load(filePrefix + '_death_inv.png').convert_alpha()
            self.deathSpriteInv = pygame.image.load(filePrefix + '_death_inv.png').convert_alpha()

            # Initialize collider
            self.collider = Physics.Collider(self.moveSprite.get_rect().size[0], self.moveSprite.get_rect().size[1], initialPosition, currentDisplayWidth, currentDisplayHeight)

            # Initialize projectile
            self.projectile = Physics.Projectile(self.character, currentDisplayWidth, self.display)

            # Initialize damage instances
            self.primaryBasicAttackDamageInstance = Physics.DamageInstance(self.moveSprite.get_rect().size[0] * 3 / 4, self.moveSprite.get_rect().size[1], 5)
            self.secondaryBasicAttackDamageInstance = Physics.DamageInstance(self.moveSprite.get_rect().size[0] * 3 / 4, self.moveSprite.get_rect().size[1], 10)

            # Initialize cooldowns
            self.primaryBasicAttackCooldown = Physics.Cooldown(0.5)
            self.secondaryBasicAttackCooldown = Physics.Cooldown(0.5)
            self.basicPowerCooldown = Physics.Cooldown(2)
            self.specialPowerCooldown = Physics.Cooldown(0)

            # Initialize actions
            self.primaryBasicAttackAction = Physics.Action(self.primaryBasicAttackSprite, self.primaryBasicAttackSpriteInv, 0.1)
            self.secondaryBasicAttackAction = Physics.Action(self.secondaryBasicAttackSprite, self.secondaryBasicAttackSpriteInv, 0.1)
            self.basicPowerAction = Physics.Action(self.basicPowerSprite, self.basicPowerSpriteInv, 0.25)
            self.specialPowerAction = Physics.Action(self.specialPowerSprite, self.specialPowerSpriteInv, 1.5)
            self.painAction = Physics.Action(self.painSprite, self.painSpriteInv, 0.1)

            self.playerCurrentAction = None

            # Player looking direction
            self.lookingDirection = lookingDirection

            if self.lookingDirection == 1:
                self.currentSprite = self.moveSprite
            elif self.lookingDirection == -1:
                self.currentSprite = self.moveSpriteInv

        def takeDamage(self, damage, direction):
            self.state = 'Damage'
            self.lookingDirection = -direction
            self.healthBar.decreaseValue(damage)
            if self.healthBar.value > 0:
                self.playerCurrentAction = self.painAction
                self.playerCurrentAction.start()
            else:
                self.state = 'Death'
            
        def render(self):
            self.display.blit(self.currentSprite, self.collider.position)

    def getRandomPreRoundMessage(self):
        preRoundMessages = ['¡Mecha, mecha, mecha!', 'Abóllense', '¡Saquense la mugre!']
        return preRoundMessages[random.randint(0, 2)]

    def preStartFight(self):
        # Set match timer
        self.timer = self.Timer(int(Option.timeLimit), self.currentDisplayWidth, self.display)
        
        # Set the players that will fight
        self.player1 = self.Player(self.player1Character, pygame.math.Vector2(100, 0), 1, self.currentDisplayWidth, self.currentDisplayHeight, self.display)
        self.player2 = self.Player(self.player2Character, pygame.math.Vector2(self.currentDisplayWidth - 200, 0), -1, self.currentDisplayWidth, self.currentDisplayHeight, self.display)

        # Set all the status bars
        self.player1.healthBar = self.Bar(100, Color.red, 50, 50, (self.currentDisplayWidth / 2) - 150, 30, 'left', self.display)
        self.player2.healthBar = self.Bar(100, Color.red, self.currentDisplayWidth - ((self.currentDisplayWidth / 2) - 150) - 50, 50, (self.currentDisplayWidth / 2) - 150, 30, 'right', self.display)
        self.player1.staminaBar = self.Bar(0, Color.blue, 50, 85, (self.currentDisplayWidth / 2) - 200, 20, 'left', self.display)
        self.player2.staminaBar = self.Bar(0, Color.blue, self.currentDisplayWidth - ((self.currentDisplayWidth / 2) - 200) - 50, 85, (self.currentDisplayWidth / 2) - 200, 20, 'right', self.display)
            
    def startFight(self):
        # Set some flags and constants
        player1Victories = 0
        player2Victories = 0
        winner = 0
        currentRound = 1
        roundResultText = ''
        roundWinnerText = ''
        currentRoundWinner = 0
        startNextRoundCooldown = Physics.Cooldown(5)
        showRoundNumberCooldown = Physics.Cooldown(5)
        matchIsActive = True
        fightOver = False
        forcedFinishTriggered = False
        waitingForNextRound = False

        while matchIsActive and not forcedFinishTriggered:
            matchIsActive = currentRound <= int(Option.rounds)
            
            if player1Victories >= math.ceil(int(Option.rounds) / 2):
                winner = 1
                matchIsActive = False
            elif player2Victories >= math.ceil(int(Option.rounds) / 2):
                winner = 2
                matchIsActive = False

            if not matchIsActive:
                if winner == 0:
                    if player1Victories == player2Victories:
                        winner = 3
                    elif player1Victories > player2Victories:
                        winner = 1
                    elif player2Victories > player1Victories:
                        winner = 2

                postFightLoop = True
                while postFightLoop:
                    # Analize events
                    mousebuttonupTriggered = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            mousebuttonupTriggered = True

                    # Draw background
                    self.display.fill(Color.white)
                    pygame.draw.rect(self.display, Color.black, (20, 20, self.currentDisplayWidth - 40, self.currentDisplayHeight - 40))

                    buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

                    # Draw the winner
                    if winner == 3:
                        Text.renderLabel('EMPATE' + str(currentRound), 'white', 'dolphins.ttf', 125, self.currentDisplayWidth / 2, 250, '', self.display)
                    else:
                        Text.renderLabel('El ganador es:', 'white', 'dolphins.ttf', 60, self.currentDisplayWidth / 2, 250, '', self.display)
                        Text.renderLabel('JUGADOR ' + str(winner), 'white', 'dolphins.ttf', 125, self.currentDisplayWidth / 2, 400, '', self.display)

                    # Listen for button clicked
                    if mousebuttonupTriggered:
                        if buttonBack.mouseInBonudaries():
                            postFightLoop = False

                    # Refresh
                    pygame.display.update()
                    self.clock.tick(20)

            else:
                preroundMessage = self.getRandomPreRoundMessage()
                showRoundNumberCooldown.start()
                waitingForNextRound = False
                self.preStartFight()
                fightOver = False
                fighting = True
                while fighting:
                    # Analize events
                    mousebuttonupTriggered = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            mousebuttonupTriggered = True

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
                        # Update looking direction
                        if self.player1.collider.isFloored:
                            if self.player1.collider.velocity[0] > 0:
                                self.player1.lookingDirection = 1
                            elif self.player1.collider.velocity[0] < 0:
                                self.player1.lookingDirection = -1
                        # Jump
                        if keysPressed[Option.controlPlayer1.jump]:
                            if self.player1.collider.isFloored:
                                self.player1.collider.velocity[1] = -30
                        # Attack
                        player1StartBasicPower = True
                        for key in Option.controlPlayer1.basicPower:
                            if not keysPressed[key]:
                                player1StartBasicPower = False
                        player1StartSpecialPower = True
                        for key in Option.controlPlayer1.specialPower:
                            if not keysPressed[key]:
                                player1StartSpecialPower = False
                        if player1StartBasicPower:
                            if not self.player1.projectile.active and self.player1.basicPowerCooldown.isReady and self.player1.collider.isFloored and (self.player1.staminaBar.value >= 5):
                                player1ProjectileInitialPositionX = self.player1.collider.position[0] + (self.player1.collider.width / 2)
                                player1ProjectileInitialPositionY = self.player1.collider.position[1] + (self.player1.collider.height / 2)
                                player1ProjectileInitialPositionVector = pygame.math.Vector2(player1ProjectileInitialPositionX, player1ProjectileInitialPositionY)
                                self.player1.projectile.fire(player1ProjectileInitialPositionVector, self.player1.lookingDirection)
                                self.player1.playerCurrentAction = self.player1.basicPowerAction
                                self.player1.playerCurrentAction.start()
                                self.player1.state = 'Attack'
                                self.player1.staminaBar.decreaseValue(5)
                                self.player1.basicPowerCooldown.start()
                        elif player1StartSpecialPower:
                            pass
                        elif keysPressed[Option.controlPlayer1.primaryBasicAttack]:
                            if self.player1.primaryBasicAttackCooldown.isReady and self.player1.collider.isFloored:
                                primaryBasicAttackDamageInstanceX = 0
                                if self.player1.lookingDirection == 1:
                                    primaryBasicAttackDamageInstanceX = self.player1.collider.position[0] + (self.player1.collider.width / 2)
                                elif self.player1.lookingDirection == -1:
                                    primaryBasicAttackDamageInstanceX = self.player1.collider.position[0] - (self.player1.collider.width / 4)
                                if self.player1.primaryBasicAttackDamageInstance.trigger(primaryBasicAttackDamageInstanceX, self.player1.collider.position[1], self.player2):
                                    self.player1.staminaBar.increaseValue(self.player1.primaryBasicAttackDamageInstance.damage)
                                    self.player2.takeDamage(self.player1.primaryBasicAttackDamageInstance.damage, self.player1.lookingDirection)
                                self.player1.playerCurrentAction = self.player1.primaryBasicAttackAction
                                self.player1.playerCurrentAction.start()
                                self.player1.state = 'Attack'
                                self.player1.primaryBasicAttackCooldown.start()
                        elif keysPressed[Option.controlPlayer1.secondaryBasicAttack]:
                            if self.player1.secondaryBasicAttackCooldown.isReady and self.player1.collider.isFloored:
                                secondaryBasicAttackDamageInstanceX = 0
                                if self.player1.lookingDirection == 1:
                                    secondaryBasicAttackDamageInstanceX = self.player1.collider.position[0] + (self.player1.collider.width / 2)
                                elif self.player1.lookingDirection == -1:
                                    secondaryBasicAttackDamageInstanceX = self.player1.collider.position[0] - (self.player1.collider.width / 4)
                                if self.player1.secondaryBasicAttackDamageInstance.trigger(secondaryBasicAttackDamageInstanceX, self.player1.collider.position[1], self.player2):
                                    self.player1.staminaBar.increaseValue(self.player1.secondaryBasicAttackDamageInstance.damage)
                                    self.player2.takeDamage(self.player1.secondaryBasicAttackDamageInstance.damage, self.player1.lookingDirection)
                                self.player1.playerCurrentAction = self.player1.secondaryBasicAttackAction
                                self.player1.playerCurrentAction.start()
                                self.player1.state = 'Attack'
                                self.player1.secondaryBasicAttackCooldown.start()
                    elif self.player1.state == 'Attack':
                        self.player1.collider.velocity[0] = 0
                    elif self.player1.state == 'Damage':
                        self.player1.collider.velocity[0] = Physics.playerStumbleSpeed * -self.player1.lookingDirection
                                
                    if self.player2.state == 'Move':
                        # Move
                        if keysPressed[Option.controlPlayer2.moveLeft] or keysPressed[Option.controlPlayer2.moveRight]:
                            if keysPressed[Option.controlPlayer2.moveLeft]:
                                self.player2.collider.velocity[0] = -Physics.playerMovementSpeed
                            elif keysPressed[Option.controlPlayer2.moveRight]:
                                self.player2.collider.velocity[0] = Physics.playerMovementSpeed
                        else:
                            self.player2.collider.velocity[0] = 0
                        # Update looking direction
                        if self.player2.collider.isFloored:
                            if self.player2.collider.velocity[0] > 0:
                                self.player2.lookingDirection = 1
                            elif self.player2.collider.velocity[0] < 0:
                                self.player2.lookingDirection = -1
                        # Jump
                        if keysPressed[Option.controlPlayer2.jump]:
                            if self.player2.collider.isFloored:
                                self.player2.collider.velocity[1] = -30
                        # Attack
                        player2StartBasicPower = True
                        for key in Option.controlPlayer2.basicPower:
                            if not keysPressed[key]:
                                player2StartBasicPower = False
                        player2StartSpecialPower = True
                        for key in Option.controlPlayer2.specialPower:
                            if not keysPressed[key]:
                                player2StartSpecialPower = False
                        if player2StartBasicPower:
                            if not self.player2.projectile.active and self.player2.basicPowerCooldown.isReady and self.player2.collider.isFloored and (self.player2.staminaBar.value >= 5):
                                player2ProjectileInitialPositionX = self.player2.collider.position[0] + (self.player2.collider.width / 2)
                                player2ProjectileInitialPositionY = self.player2.collider.position[1] + (self.player2.collider.height / 2)
                                player2ProjectileInitialPositionVector = pygame.math.Vector2(player2ProjectileInitialPositionX, player2ProjectileInitialPositionY)
                                self.player2.projectile.fire(player2ProjectileInitialPositionVector, self.player2.lookingDirection)
                                self.player2.playerCurrentAction = self.player2.basicPowerAction
                                self.player2.playerCurrentAction.start()
                                self.player2.state = 'Attack'
                                self.player1.staminaBar.decreaseValue(5)
                                self.player2.basicPowerCooldown.start()
                        elif player2StartSpecialPower:
                            pass
                        elif keysPressed[Option.controlPlayer2.primaryBasicAttack]:
                            if self.player2.primaryBasicAttackCooldown.isReady and self.player2.collider.isFloored:
                                primaryBasicAttackDamageInstanceX = 0
                                if self.player2.lookingDirection == 1:
                                    primaryBasicAttackDamageInstanceX = self.player2.collider.position[0] + (self.player2.collider.width / 2)
                                elif self.player2.lookingDirection == -1:
                                    primaryBasicAttackDamageInstanceX = self.player2.collider.position[0] - (self.player2.collider.width / 4)
                                if self.player2.primaryBasicAttackDamageInstance.trigger(primaryBasicAttackDamageInstanceX, self.player2.collider.position[1], self.player1):
                                    self.player2.staminaBar.increaseValue(self.player2.primaryBasicAttackDamageInstance.damage)
                                    self.player1.takeDamage(self.player2.primaryBasicAttackDamageInstance.damage, self.player2.lookingDirection)
                                self.player2.playerCurrentAction = self.player2.primaryBasicAttackAction
                                self.player2.playerCurrentAction.start()
                                self.player2.state = 'Attack'
                                self.player2.primaryBasicAttackCooldown.start()
                        elif keysPressed[Option.controlPlayer2.secondaryBasicAttack]:
                            if self.player2.secondaryBasicAttackCooldown.isReady and self.player2.collider.isFloored:
                                secondaryBasicAttackDamageInstanceX = 0
                                if self.player2.lookingDirection == 1:
                                    secondaryBasicAttackDamageInstanceX = self.player2.collider.position[0] + (self.player2.collider.width / 2)
                                elif self.player2.lookingDirection == -1:
                                    secondaryBasicAttackDamageInstanceX = self.player2.collider.position[0] - (self.player2.collider.width / 4)
                                if self.player2.secondaryBasicAttackDamageInstance.trigger(secondaryBasicAttackDamageInstanceX, self.player2.collider.position[1], self.player1):
                                    self.player2.staminaBar.increaseValue(self.player2.secondaryBasicAttackDamageInstance.damage)
                                    self.player1.takeDamage(self.player1.secondaryBasicAttackDamageInstance.damage, self.player2.lookingDirection)
                                self.player2.playerCurrentAction = self.player2.secondaryBasicAttackAction
                                self.player2.playerCurrentAction.start()
                                self.player2.state = 'Attack'
                                self.player2.secondaryBasicAttackCooldown.start()
                    elif self.player2.state == 'Attack':
                        self.player2.collider.velocity[0] = 0
                    elif self.player2.state == 'Damage':
                        self.player2.collider.velocity[0] = Physics.playerStumbleSpeed * -self.player2.lookingDirection

                    # Update colliders
                    self.player1.collider.move()
                    self.player2.collider.move()

                    # Update projectiles
                    if self.player1.projectile.active:
                        self.player1.projectile.move(self.player2)
                        if self.player1.projectile.isCollidingTargetPlayer:
                            self.player1.projectile.active = False
                            self.player2.takeDamage(Physics.Projectile.damage, self.player1.projectile.shootingDirection)
                    if self.player2.projectile.active:
                        self.player2.projectile.move(self.player1)
                        if self.player2.projectile.isCollidingTargetPlayer:
                            self.player2.projectile.active = False
                            self.player1.takeDamage(Physics.Projectile.damage, self.player2.projectile.shootingDirection)
                        
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
                    elif self.player1.state == 'Death':
                        if self.player1.lookingDirection == 1:
                            self.player1.currentSprite = self.player1.deathSprite
                        elif self.player1.lookingDirection == -1:
                            self.player1.currentSprite = self.player1.deathSpriteInv
                    elif self.player1.playerCurrentAction != None:
                        if self.player1.lookingDirection == 1:
                            self.player1.currentSprite = self.player1.playerCurrentAction.sprite
                        elif self.player1.lookingDirection == -1:
                            self.player1.currentSprite = self.player1.playerCurrentAction.spriteInv

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
                    elif self.player2.state == 'Death':
                        if self.player2.lookingDirection == 1:
                            self.player2.currentSprite = self.player2.deathSprite
                        elif self.player2.lookingDirection == -1:
                            self.player2.currentSprite = self.player2.deathSpriteInv
                    elif self.player2.playerCurrentAction != None:
                        if self.player2.lookingDirection == 1:
                            self.player2.currentSprite = self.player2.playerCurrentAction.sprite
                        elif self.player2.lookingDirection == -1:
                            self.player2.currentSprite = self.player2.playerCurrentAction.spriteInv

                    # Update cooldowns
                    self.player1.primaryBasicAttackCooldown.tick(60)
                    self.player1.secondaryBasicAttackCooldown.tick(60)
                    self.player1.basicPowerCooldown.tick(60)
                    self.player1.specialPowerCooldown.tick(60)
                    self.player2.primaryBasicAttackCooldown.tick(60)
                    self.player2.secondaryBasicAttackCooldown.tick(60)
                    self.player2.basicPowerCooldown.tick(60)
                    self.player2.specialPowerCooldown.tick(60)
                    showRoundNumberCooldown.tick(60)
                    startNextRoundCooldown.tick(60)

                    # Update current actions
                    if self.player1.playerCurrentAction != None:
                        self.player1.playerCurrentAction.tick(60)
                    if self.player2.playerCurrentAction != None:
                        self.player2.playerCurrentAction.tick(60)

                    # Update states
                    if self.player1.playerCurrentAction != None:
                        if self.player1.playerCurrentAction.done and self.player1.state != 'Death':
                            self.player1.state = 'Move'
                    if self.player2.playerCurrentAction != None:
                        if self.player2.playerCurrentAction.done and self.player2.state != 'Death':
                            self.player2.state = 'Move'

                    # Check for match over
                    if not fightOver:
                        if self.timer.value == 0:
                            fightOver = True
                            roundResultText = 'Tiempo'
                            if self.player1.staminaBar.value == self.player2.staminaBar.value:
                                player1Victories = player1Victories + 1
                                player2Victories + player2Victories + 1
                                roundWinnerText = 'Empate'
                            elif self.player1.staminaBar.value > self.player2.staminaBar.value:
                                player1Victories = player1Victories + 1
                                roundWinnerText = 'Ganó el Jugador 1'
                            elif self.player1.staminaBar.value < self.player2.staminaBar.value:
                                player2Victories + player2Victories + 1
                                roundWinnerText = 'Ganó el Jugador 2'
                        elif self.player1.state == 'Death' and self.player2.state == 'Death':
                            fightOver = True
                            player1Victories = player1Victories + 1
                            player2Victories + player2Victories + 1
                            roundResultText = 'K.O.'
                            roundWinnerText = 'Empate'
                        elif self.player1.state == 'Death':
                            fightOver = True
                            player2Victories = player2Victories + 1
                            roundResultText = 'K.O.'
                            roundWinnerText = 'Ganó el Jugador 2'
                        elif self.player2.state == 'Death':
                            fightOver = True
                            player1Victories = player1Victories + 1
                            roundResultText = 'K.O.'
                            roundWinnerText = 'Ganó el Jugador 1'
                    if fightOver:
                        if not waitingForNextRound:
                            currentRound = currentRound + 1
                            startNextRoundCooldown.start()
                            waitingForNextRound = True
                        elif startNextRoundCooldown.isReady:
                            fighting = False
                    else:
                        # Update timer
                        self.timer.tick(60)
                    
                    # Draw the scenario
                    self.display.blit(self.scenario, (0, 0))
                    self.player1.healthBar.render()
                    self.player2.healthBar.render()
                    self.player1.staminaBar.render()
                    self.player2.staminaBar.render()
                    self.timer.render()
                    buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, (self.currentDisplayWidth / 2) - 75, 5, 150, 30, self.display)

                    # Render the players
                    self.player1.render()
                    self.player2.render()

                    # Render the projectiles
                    if self.player1.projectile.active:
                        self.player1.projectile.render()
                    if self.player2.projectile.active:
                        self.player2.projectile.render()

                    # If match is over, draw the results
                    if fightOver:
                        pygame.draw.rect(self.display, Color.black, (0, 150, self.currentDisplayWidth, 300))
                        Text.renderLabel(roundResultText, 'white', 'dolphins.ttf', 125, self.currentDisplayWidth / 2, 250, '', self.display)
                        Text.renderLabel(roundWinnerText, 'white', 'dolphins.ttf', 60, self.currentDisplayWidth / 2, 400, '', self.display)

                    # Draw current round slogan
                    if not showRoundNumberCooldown.isReady:
                        pygame.draw.rect(self.display, Color.black, (0, 150, self.currentDisplayWidth, 300))
                        Text.renderLabel('ROUND ' + str(currentRound), 'white', 'dolphins.ttf', 125, self.currentDisplayWidth / 2, 250, '', self.display)
                        Text.renderLabel(preroundMessage, 'white', 'dolphins.ttf', 60, self.currentDisplayWidth / 2, 400, '', self.display)

                    # Listen for button clicked
                    if mousebuttonupTriggered:
                        if buttonBack.mouseInBonudaries():
                            fighting = False
                            forcedFinishTriggered = True

                    # Render all
                    pygame.display.flip()

                    # Refresh
                    pygame.display.update()
                    self.clock.tick(60)