#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from Modules.Text import *

class Option():
    class Control():
        def __init__(self, moveUp, moveDown, moveLeft, moveRight, jump, primaryBasicAttack, secondaryBasicAttack):
            self.moveUp = moveUp
            self.moveDown = moveDown
            self.moveLeft = moveLeft
            self.moveRight = moveRight
            self.jump = jump
            self.primaryBasicAttack = primaryBasicAttack
            self.secondaryBasicAttack = secondaryBasicAttack
            self.basicPower = [self.moveUp, self.primaryBasicAttack]
            self.specialPower = [self.moveUp, self.secondaryBasicAttack]

        def updateBasicSpecialPower(self):
            self.basicPower = [self.moveUp, self.primaryBasicAttack]
            self.specialPower = [self.moveUp, self.secondaryBasicAttack]

    class NumericUpDown():
        def __init__(self, text, color, fontFamily, fontSize, backgroundColor, backgroundColorHover, x, y, height, display):
            self.x = x 
            self.y = y
            self.height = height

            mousePos = pygame.mouse.get_pos()
            # Above left arrow
            if self.x + 25 > mousePos[0] > self.x and self.y + self.height > mousePos[1] > self.y:
                # Left arrow
                pygame.draw.polygon(display, backgroundColorHover, ((self.x + 25, self.y + self.height), (self.x + 25, self.y), (self.x, self.y + (self.height / 2)), 25))
                # Text
                Text.renderLabel(text, color, fontFamily, fontSize, self.x + 80, self.y + (self.height / 2), '', display)
                # Right arrow
                pygame.draw.polygon(display, backgroundColor, ((self.x + 135, self.y + self.height), (self.x + 135, self.y), (self.x + 160, self.y + (self.height / 2)), 25))
            # Above right arrow
            elif self.x + 160 > mousePos[0] > self.x + 135 and self.y + self.height > mousePos[1] > self.y:
                # Left arrow
                pygame.draw.polygon(display, backgroundColor, ((self.x + 25, self.y + self.height), (self.x + 25, self.y), (self.x, self.y + (self.height / 2)), 25))
                # Text
                Text.renderLabel(text, color, fontFamily, fontSize, self.x + 80, self.y + (self.height / 2), '', display)
                # Right arrow
                pygame.draw.polygon(display, backgroundColorHover, ((self.x + 135, self.y + self.height), (self.x + 135, self.y), (self.x + 160, self.y + (self.height / 2)), 25))
            else:
                # Left arrow
                pygame.draw.polygon(display, backgroundColor, ((self.x + 25, self.y + self.height), (self.x + 25, self.y), (self.x, self.y + (self.height / 2)), 25))
                # Text
                Text.renderLabel(text, color, fontFamily, fontSize, self.x + 80, self.y + (self.height / 2), '', display)
                # Right arrow
                pygame.draw.polygon(display, backgroundColor, ((self.x + 135, self.y + self.height), (self.x + 135, self.y), (self.x + 160, self.y + (self.height / 2)), 25))

        def mouseAboveLeftArrow(self):
            mousePos = pygame.mouse.get_pos()
            return (self.x + 25 > mousePos[0] > self.x and self.y + self.height > mousePos[1] > self.y)

        def mouseAboveRightArrow(self):
            mousePos = pygame.mouse.get_pos()
            return (self.x + 160 > mousePos[0] > self.x + 135 and self.y + self.height > mousePos[1] > self.y)

    # Static variables
    volume = 0.50
    timeLimit = 180
    rounds = 3
    controlPlayer1 = Control(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_l, pygame.K_i, pygame.K_o)
    controlPlayer2 = Control(pygame.K_r, pygame.K_f, pygame.K_d, pygame.K_g, pygame.K_x, pygame.K_a, pygame.K_s)

    @staticmethod
    def keyIsRepeated(keyCode):
        result = False
        if Option.controlPlayer1.moveUp == keyCode:
            result = True
        elif Option.controlPlayer1.moveDown == keyCode:
            result = True
        elif Option.controlPlayer1.moveLeft == keyCode:
            result = True
        elif Option.controlPlayer1.moveRight == keyCode:
            result = True
        elif Option.controlPlayer1.jump == keyCode:
            result = True
        elif Option.controlPlayer1.primaryBasicAttack == keyCode:
            result = True
        elif Option.controlPlayer1.secondaryBasicAttack == keyCode:
            result = True
        elif Option.controlPlayer2.moveUp == keyCode:
            result = True
        elif Option.controlPlayer2.moveDown == keyCode:
            result = True
        elif Option.controlPlayer2.moveLeft == keyCode:
            result = True
        elif Option.controlPlayer2.moveRight == keyCode:
            result = True
        elif Option.controlPlayer2.jump == keyCode:
            result = True
        elif Option.controlPlayer2.primaryBasicAttack == keyCode:
            result = True
        elif Option.controlPlayer2.secondaryBasicAttack == keyCode:
            result = True
        return result