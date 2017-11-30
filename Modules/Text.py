#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import os

class Text:
    # Static variables
    fontPath = 'Resources/Fonts/'

    @staticmethod
    def renderLabel(text, color, fontFamily, fontSize, x, y, align, display):
        font = pygame.font.Font(Text.fontPath + fontFamily, fontSize)
        label = font.render(text, True, pygame.Color(color))

        if align == 'topleft':
            labelRect = label.get_rect(topleft = (x, y))
        elif align == 'topright':
            labelRect = label.get_rect(topright = (x, y))
        else:
            labelRect = label.get_rect()
            labelRect.center = (x, y)

        display.blit(label, labelRect)