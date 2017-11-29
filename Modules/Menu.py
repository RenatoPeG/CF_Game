import ctypes
import pygame
import sys
from Modules.Button import *
from Modules.Color import *
from Modules.Image import *
from Modules.Key import *
from Modules.Music import *
from Modules.Option import *
from Modules.Physics import *
from Modules.Proxy import *
from Modules.Text import *
pygame.init()

class Menu:
    def __init__(self):
        # Set display starting configuration
        self.currentDisplayWidth = 1200
        self.currentDisplayHeight = 700

        # Set display
        self.display = pygame.display.set_mode((self.currentDisplayWidth, self.currentDisplayHeight))
        pygame.display.set_caption('Cholo Fighter')

        # Set clock
        self.clock = pygame.time.Clock()

        # Load characters and scenarios from the server
        try:
            self.characters = Proxy.getCharacters()
            self.scenarios = Proxy.getScenarios()
        except:
            raise SystemExit('No se pudo conectar con el servidor.')

        # Play music and set volume
        Music.playSong(1)
        Music.setVolume(Option.volume)

        # Current character being chosen by each player
        self.player1Character = {'name': ''}
        self.player2Character = {'name': ''}

        # Current scenario being chosen
        self.scenario = {'name': ''}

        # Current player being configured in the configure player menu
        self.configuredPlayer = 1

        # Current key being configured in the configure player menu
        self.configureKeyId = None

    def gameMenu(self):
        gameMenuLoop = True
        while gameMenuLoop:
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
            
            # Load the logo
            logo, logoRect = Image.loadImage('logo.png')
            logoRect.center = (self.currentDisplayWidth / 2, self.currentDisplayHeight * 0.65)
            self.display.blit(logo, logoRect)

            # Draw buttons
            buttonPlay = Button('Jugar', 'white', 'dolphins.ttf', 35, Color.black, Color.brightGreen, 150, 45, 250, 50, self.display)
            buttonMusic = Button('Musica', 'white', 'dolphins.ttf', 35, Color.black, Color.brightGreen, self.currentDisplayWidth - 400, 45, 250, 50, self.display)
            buttonQuit = Button('Salir', 'white', 'dolphins.ttf', 35, Color.black, Color.red, 150, 115, 250, 50, self.display)
            buttonOptions = Button('Opciones', 'white', 'dolphins.ttf', 35, Color.black, Color.brightGreen, self.currentDisplayWidth - 400, 115, 250, 50, self.display)
            buttonTop10 = Button('Top 10', 'white', 'dolphins.ttf', 35, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 125, 45, 250, 50, self.display)

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonPlay.mouseInBonudaries():
                    self.gameCharacterSelection()
                elif buttonMusic.mouseInBonudaries():
                    Music.toggleMusic()
                elif buttonQuit.mouseInBonudaries():
                    gameMenuLoop = False
                    pygame.quit()
                    sys.exit()
                elif buttonOptions.mouseInBonudaries():
                    self.gameOptions()
                elif buttonTop10.mouseInBonudaries():
                    self.gameTop10()

            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameCharacterSelection(self):
        gameCharacterSelectionLoop = True
        while gameCharacterSelectionLoop:
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

            # List characters
            characterButtons = []
            if (len(self.characters) < 2):
                characterButtons.append(Button(self.characters[0]['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, (self.currentDisplayWidth / 2) - 100, 200, 200, 50, self.display))
            else:
                rowIndex = 0;
                columnIndex = 0;
                for i in range(0, len(self.characters) - 1):
                    character = self.characters[i]
                    if (columnIndex == 2):
                        rowIndex = rowIndex + 1
                        columnIndex = 0
                    if (columnIndex == 0):
                        x = (self.currentDisplayWidth / 4) - 100
                    elif (columnIndex == 1):
                        x = (self.currentDisplayWidth * 3 / 4) - 100

                    y = 150 + (rowIndex * 100)

                    characterButtons.append(Button(character['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, x, y, 200, 50, self.display))

                    columnIndex = columnIndex + 1
                character = self.characters[len(self.characters) - 1]
                if (len(self.characters) % 2 == 0):
                    x = (self.currentDisplayWidth * 3 / 4) - 100
                    y = 150 + (rowIndex * 100)
                    characterButtons.append(Button(character['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, x, y, 200, 50, self.display))
                else:
                    rowIndex = rowIndex + 1
                    x = (self.currentDisplayWidth / 2) - 100
                    y = 150 + (rowIndex * 100)
                    characterButtons.append(Button(character['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, x, y, 200, 50, self.display))
                
            # Draw rest of menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            Text.renderLabel('Selección de personajes', 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            Text.renderLabel(self.player1Character['name'], 'white', 'dolphins.ttf', 50, self.currentDisplayWidth / 4, 550, '', self.display)            
            Text.renderLabel('VS', 'white', 'dolphins.ttf', 65, self.currentDisplayWidth / 2, 550, '', self.display)
            Text.renderLabel(self.player2Character['name'], 'white', 'dolphins.ttf', 50, self.currentDisplayWidth * 3 / 4, 550, '', self.display)

            buttonContinue = Button('CONTINUAR', 'white', 'dolphins.ttf', 36, Color.black, Color.brightOrange, (self.currentDisplayWidth / 2) - 150, 600, 300, 75, self.display)

            # Listen for button clicked
            characterButtonClicked = False
            clickedCharacterButtonIndex = 0
            index = 0
            while (not characterButtonClicked and (index < len(characterButtons))):
                if characterButtons[index].mouseInBonudaries():
                    clickedCharacterButtonIndex = index
                    characterButtonClicked = True
                else:
                    index = index + 1

            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    # Wipe the players
                    self.player1Character = {'name': ''}
                    self.player2Character = {'name': ''}
                    gameCharacterSelectionLoop = False
                elif characterButtonClicked:
                    if (self.player1Character['name'] == ''):
                        self.player1Character = self.characters[clickedCharacterButtonIndex]
                    elif (self.player2Character['name'] == ''):
                        self.player2Character = self.characters[clickedCharacterButtonIndex]
                elif buttonContinue.mouseInBonudaries():
                    if (self.player1Character['name'] != '' and self.player2Character['name'] != ''):
                        self.gameScenarioSelection()
                        gameCharacterSelectionLoop = False

            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameScenarioSelection(self):
        gameScenarioSelectionLoop = True
        while gameScenarioSelectionLoop:
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

            # List scenarios
            scenarioButtons = []
            if (len(self.scenarios) < 2):
                scenarioButtons.append(Button(self.scenarios[0]['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, (self.currentDisplayWidth / 2) - 150, 200, 300, 50, self.display))
            else:
                rowIndex = 0;
                columnIndex = 0;
                for i in range(0, len(self.scenarios) - 1):
                    scenario = self.scenarios[i]
                    if (columnIndex == 2):
                        rowIndex = rowIndex + 1
                        columnIndex = 0
                    if (columnIndex == 0):
                        x = (self.currentDisplayWidth / 4) - 150
                    elif (columnIndex == 1):
                        x = (self.currentDisplayWidth * 3 / 4) - 150

                    y = 150 + (rowIndex * 100)

                    scenarioButtons.append(Button(scenario['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, x, y, 300, 50, self.display))

                    columnIndex = columnIndex + 1
                scenario = self.scenarios[len(self.scenarios) - 1]
                if (len(self.scenarios) % 2 == 0):
                    x = (self.currentDisplayWidth * 3 / 4) - 150
                    y = 150 + (rowIndex * 100)
                    scenarioButtons.append(Button(scenario['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, x, y, 300, 50, self.display))
                else:
                    rowIndex = rowIndex + 1
                    x = (self.currentDisplayWidth / 2) - 150
                    y = 150 + (rowIndex * 100)
                    scenarioButtons.append(Button(scenario['name'], 'white', 'dolphins.ttf', 36, Color.black, Color.red, x, y, 300, 50, self.display))

            # Draw rest of menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            Text.renderLabel('Selección de escenario', 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            Text.renderLabel(self.scenario['name'], 'white', 'dolphins.ttf', 65, self.currentDisplayWidth / 2, 550, '', self.display)

            buttonStart = Button('COMENZAR', 'white', 'dolphins.ttf', 36, Color.black, Color.brightOrange, (self.currentDisplayWidth / 2) - 150, 600, 300, 75, self.display)

            # Listen for button clicked
            scenarioButtonClicked = False
            clickedScenarioButtonIndex = 0
            index = 0
            while (not scenarioButtonClicked and (index < len(scenarioButtons))):
                if scenarioButtons[index].mouseInBonudaries():
                    clickedScenarioButtonIndex = index
                    scenarioButtonClicked = True
                else:
                    index = index + 1

            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    self.player1Character = {'name': ''}
                    self.player2Character = {'name': ''}
                    gameScenarioSelectionLoop = False
                elif scenarioButtonClicked:
                    if (self.scenario['name'] == ''):
                        self.scenario = self.scenarios[clickedScenarioButtonIndex]
                elif buttonStart.mouseInBonudaries():
                    if self.scenario['name'] != '':
                        match = Physics(self.display, self.currentDisplayWidth, self.currentDisplayHeight, self.player1Character, self.player2Character, self.scenario['asset_prefix'])
                        match.startFight()
                        # When match is over, wipe the players and the scenario
                        self.player1Character = {'name': ''}
                        self.player2Character = {'name': ''}
                        self.scenario = {'name': ''}
                        # Also set the music back to the menu track
                        Music.playSong(1)
                        Music.setVolume(Option.volume)
                        # Return to game menu
                        gameScenarioSelectionLoop = False

            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameConfigurePlayer(self):
        gameConfigurePlayerLoop = True
        while gameConfigurePlayerLoop:
             # Analize events
            mousebuttonupTriggered = False
            keydownTriggered = False
            keydownValue = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousebuttonupTriggered = True
                    if event.type == pygame.KEYDOWN:
                        keydownTriggered = True
                        keydownValue = event.key

            # Draw background
            self.display.fill(Color.white)
            pygame.draw.rect(self.display, Color.black, (20, 20, self.currentDisplayWidth - 40, self.currentDisplayHeight - 40))

            # Draw menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            buttonDefaults = Button('Reestablecer', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, self.currentDisplayWidth - 180, 30, 150, 30, self.display)

            Text.renderLabel('Configuración Jugador %s' % str(self.configuredPlayer), 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            # First Column
            Text.renderLabel('Movimiento', 'white', 'dolphins.ttf', 32, 50, 200, 'topleft', self.display)

            Text.renderLabel('Arriba', 'white', 'dolphins.ttf', 24, 50, 250, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveUp = Button('...' if self.configureKeyId == 1 else Key.getKeyLabel(Option.controlPlayer1.moveUp), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 250, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveUp = Button('...' if self.configureKeyId == 1 else Key.getKeyLabel(Option.controlPlayer2.moveUp), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 250, 150, 30, self.display)

            Text.renderLabel('Abajo', 'white', 'dolphins.ttf', 24, 50, 300, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveDown = Button('...' if self.configureKeyId == 2 else Key.getKeyLabel(Option.controlPlayer1.moveDown), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 300, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveDown = Button('...' if self.configureKeyId == 2 else Key.getKeyLabel(Option.controlPlayer2.moveDown), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 300, 150, 30, self.display)
            
            Text.renderLabel('Izquierda', 'white', 'dolphins.ttf', 24, 50, 350, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveLeft = Button('...' if self.configureKeyId == 3 else Key.getKeyLabel(Option.controlPlayer1.moveLeft), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 350, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveLeft = Button('...' if self.configureKeyId == 3 else Key.getKeyLabel(Option.controlPlayer2.moveLeft), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 350, 150, 30, self.display)
            
            Text.renderLabel('Derecha', 'white', 'dolphins.ttf', 24, 50, 400, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonMoveRight = Button('...' if self.configureKeyId == 4 else Key.getKeyLabel(Option.controlPlayer1.moveRight), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 400, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonMoveRight = Button('...' if self.configureKeyId == 4 else Key.getKeyLabel(Option.controlPlayer2.moveRight), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 400, 150, 30, self.display)
            
            Text.renderLabel('Saltar', 'white', 'dolphins.ttf', 24, 50, 450, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonJump = Button('...' if self.configureKeyId == 5 else Key.getKeyLabel(Option.controlPlayer1.jump), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 450, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonJump = Button('...' if self.configureKeyId == 5 else Key.getKeyLabel(Option.controlPlayer2.jump), 'white', 'arial.ttf', 24, Color.black, Color.blue, (self.currentDisplayWidth / 2) - 200, 450, 150, 30, self.display)
            
            # Second column
            Text.renderLabel('Ataque básico', 'white', 'dolphins.ttf', 32, (self.currentDisplayWidth / 2) + 50, 200, 'topleft', self.display)

            Text.renderLabel('Primario', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 250, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonPrimaryBasicAttack = Button('...' if self.configureKeyId == 6 else Key.getKeyLabel(Option.controlPlayer1.primaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 250, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonPrimaryBasicAttack = Button('...' if self.configureKeyId == 6 else Key.getKeyLabel(Option.controlPlayer2.primaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 250, 150, 30, self.display)
            
            Text.renderLabel('Secundario', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 300, 'topleft', self.display)
            if self.configuredPlayer == 1:
                buttonSecondaryBasicAttack = Button('...' if self.configureKeyId == 7 else Key.getKeyLabel(Option.controlPlayer1.secondaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 300, 150, 30, self.display)
            elif self.configuredPlayer == 2:
                buttonSecondaryBasicAttack = Button('...' if self.configureKeyId == 7 else Key.getKeyLabel(Option.controlPlayer2.secondaryBasicAttack), 'white', 'arial.ttf', 24, Color.black, Color.blue, self.currentDisplayWidth - 200, 300, 150, 30, self.display)
            
            Text.renderLabel('Poder', 'white', 'dolphins.ttf', 32, (self.currentDisplayWidth / 2) + 50, 350, 'topleft', self.display)

            Text.renderLabel('Básico', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 400, 'topleft', self.display)
            keyCombination = ''
            started = False
            if self.configuredPlayer == 1:
                for key in Option.controlPlayer1.basicPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            elif self.configuredPlayer == 2:
                for key in Option.controlPlayer2.basicPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            Text.renderLabel(keyCombination, 'white', 'arial.ttf', 24, self.currentDisplayWidth - 55, 400, 'topright', self.display)

            Text.renderLabel('Especial', 'white', 'dolphins.ttf', 24, (self.currentDisplayWidth / 2) + 50, 450, 'topleft', self.display)
            keyCombination = ''
            started = False
            if self.configuredPlayer == 1:
                for key in Option.controlPlayer1.specialPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            elif self.configuredPlayer == 2:
                for key in Option.controlPlayer2.specialPower:
                    if started:
                        keyCombination += ' + ' + Key.getKeyLabel(key)
                    else:
                        keyCombination += Key.getKeyLabel(key)
                        started = True
            Text.renderLabel(keyCombination, 'white', 'arial.ttf', 24, self.currentDisplayWidth - 55, 450, 'topright', self.display)

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    self.configureKeyId = None
                    gameConfigurePlayerLoop = False
                elif buttonDefaults.mouseInBonudaries():
                    # Player controls
                    if self.configuredPlayer == 1:
                        Option.controlPlayer1 = Option.Control(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_l, pygame.K_i, pygame.K_o)
                    elif self.configuredPlayer == 2:
                        Option.controlPlayer2 = Option.Control(pygame.K_r, pygame.K_f, pygame.K_d, pygame.K_g, pygame.K_x, pygame.K_a, pygame.K_s)
                elif self.configureKeyId == None:
                    if buttonMoveUp.mouseInBonudaries():
                        self.configureKeyId = 1
                    if buttonMoveDown.mouseInBonudaries():
                        self.configureKeyId = 2
                    if buttonMoveLeft.mouseInBonudaries():
                        self.configureKeyId = 3
                    if buttonMoveRight.mouseInBonudaries():
                        self.configureKeyId = 4
                    if buttonJump.mouseInBonudaries():
                        self.configureKeyId = 5
                    if buttonPrimaryBasicAttack.mouseInBonudaries():
                        self.configureKeyId = 6
                    if buttonSecondaryBasicAttack.mouseInBonudaries():
                        self.configureKeyId = 7
            # Listen for key pressed
            if keydownTriggered:
                if self.configureKeyId != None:
                    if self.configureKeyId == 1:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveUp = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveUp = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 2:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveDown = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveDown = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 3:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveLeft = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveLeft = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 4:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.moveRight = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.moveRight = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 5:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.jump = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.jump = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 6:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.primaryBasicAttack = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.primaryBasicAttack = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    if self.configureKeyId == 7:
                        if self.configuredPlayer == 1:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer1.secondaryBasicAttack = keydownValue
                                Option.controlPlayer1.updateBasicSpecialPower()
                            self.configureKeyId = None
                        elif self.configuredPlayer == 2:
                            if not Option.keyIsRepeated(keydownValue):
                                Option.controlPlayer2.secondaryBasicAttack = keydownValue
                                Option.controlPlayer2.updateBasicSpecialPower()
                            self.configureKeyId = None
                    
            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameOptions(self):
        gameOptionsLoop = True
        while gameOptionsLoop:
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

            # Draw menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            buttonDefaults = Button('Reestablecer', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, self.currentDisplayWidth - 180, 30, 150, 30, self.display)

            Text.renderLabel('Opciones', 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            Text.renderLabel('Volumen', 'white', 'dolphins.ttf', 36, 50, 275, 'topleft', self.display)
            numericUpDownVolume = Option.NumericUpDown(str(int(Option.volume * 100)) + '%', 'white', 'dolphins.ttf', 36, Color.brightRed, Color.red, self.currentDisplayWidth - 205, 275, 30, self.display)

            Text.renderLabel('Tiempo límite', 'white', 'dolphins.ttf', 36, 50, 350, 'topleft', self.display)
            numericUpDownTimeLimit = Option.NumericUpDown(str(Option.timeLimit), 'white', 'dolphins.ttf', 36, Color.brightRed, Color.red, self.currentDisplayWidth - 205, 350, 30, self.display)

            Text.renderLabel('Número de rounds', 'white', 'dolphins.ttf', 36, 50, 425, 'topleft', self.display)
            numericUpDownRounds = Option.NumericUpDown(str(Option.rounds), 'white', 'dolphins.ttf', 36, Color.brightRed, Color.red, self.currentDisplayWidth - 205, 425, 30, self.display)

            Text.renderLabel('Controles Jugador 1', 'white', 'dolphins.ttf', 36, 50, 500, 'topleft', self.display)
            buttonConfigurePlayer1 = Button('Configurar', 'white', 'dolphins.ttf', 36, Color.black, Color.blue, self.currentDisplayWidth - 245, 500, 200, 50, self.display)

            Text.renderLabel('Controles Jugador 2', 'white', 'dolphins.ttf', 36, 50, 575, 'topleft', self.display)
            buttonConfigurePlayer2 = Button('Configurar', 'white', 'dolphins.ttf', 36, Color.black, Color.blue, self.currentDisplayWidth - 245, 575, 200, 50, self.display)

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    gameOptionsLoop = False
                elif buttonDefaults.mouseInBonudaries():
                    # Volume
                    Option.volume = 0.50
                    Music.setVolume(Option.volume)
                    # Time limit                    
                    Option.timeLimit = 180
                    # Rounds
                    Option.rounds = 3
                elif numericUpDownVolume.mouseAboveLeftArrow():
                    if round(Option.volume, 2) >= 0.05:
                        Option.volume -= 0.05
                        Music.setVolume(Option.volume)
                elif numericUpDownVolume.mouseAboveRightArrow():
                    if round(Option.volume, 2) <= 0.95:
                        Option.volume += 0.05
                        Music.setVolume(Option.volume)
                elif numericUpDownTimeLimit.mouseAboveLeftArrow():
                    if int(Option.timeLimit) >= 45:
                        Option.timeLimit = str(int(Option.timeLimit) - 15)
                elif numericUpDownTimeLimit.mouseAboveRightArrow():
                    if int(Option.timeLimit) <= 165:
                        Option.timeLimit = str(int(Option.timeLimit) + 15)
                elif numericUpDownRounds.mouseAboveLeftArrow():
                    if int(Option.rounds) >= 2:
                        Option.rounds = str(int(Option.rounds) - 1)
                elif numericUpDownRounds.mouseAboveRightArrow():
                    if int(Option.rounds) <= 4:
                        Option.rounds = str(int(Option.rounds) + 1)
                elif buttonConfigurePlayer1.mouseInBonudaries():
                    self.configuredPlayer = 1
                    self.gameConfigurePlayer()
                elif buttonConfigurePlayer2.mouseInBonudaries():
                    self.configuredPlayer = 2
                    self.gameConfigurePlayer()

            # Refresh
            pygame.display.update()
            self.clock.tick(20)

    def gameTop10(self):
        gameTop10Loop = True
        while gameTop10Loop:
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

            # Draw menu content
            buttonBack = Button('Regresar', 'white', 'dolphins.ttf', 20, Color.black, Color.brightOrange, 30, 30, 150, 30, self.display)

            Text.renderLabel('Top 10', 'white', 'dolphins.ttf', 70, self.currentDisplayWidth / 2, 100, '', self.display)

            scores = Proxy.getScores()
            if len(scores) == 0:
                Text.renderLabel('No hay puntuaciones, ¡sé el primero!', 'white', 'arial.ttf', 20, self.currentDisplayWidth / 2, 200, '', self.display)
            else:
                if len(scores) > 1:
                    # Bubble to sort scores
                    for i in range(1, len(scores)):
                        for j in range(0, len(scores) - i):
                            if(scores[j]['score'] < scores[j + 1]['score']):
                                k = scores[j + 1]
                                scores[j + 1] = scores[j]
                                scores[j] = k;
                y = 200
                for score in scores:
                    Text.renderLabel(score['name'], 'white', 'arial.ttf', 20, 100, y, 'topleft', self.display)
                    Text.renderLabel(str(score['score']), 'white', 'arial.ttf', 20, self.currentDisplayWidth - 100, y, 'topright', self.display)
                    y = y + 30

            # Listen for button clicked
            if mousebuttonupTriggered:
                if buttonBack.mouseInBonudaries():
                    gameTop10Loop = False

            # Refresh
            pygame.display.update()
            self.clock.tick(20)