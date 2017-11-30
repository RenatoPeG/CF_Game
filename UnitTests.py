#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import unittest
from Modules.Color import *
from Modules.Option import *
from Modules.Physics import *
from Modules.Proxy import *

class TestCholoFighter(unittest.TestCase):
	# Test if player takes damage
	def test_player_damage(self):
		display = pygame.display.set_mode((1, 1))
		player = Physics.Player({'name': 'Melcochita', 'asset_prefix': 'melcochita'}, pygame.math.Vector2(0, 0), 1, 1, 1, display)
		player.healthBar = Physics.Bar(100, Color.red, 0, 0, 1, 1, 'left', display)
		player.takeDamage(25, 1)
		self.assertEqual(player.healthBar.value, 75)

	# Test if player dies
	def test_player_die(self):
		display = pygame.display.set_mode((1, 1))
		player = Physics.Player({'name': 'Melcochita', 'asset_prefix': 'melcochita'}, pygame.math.Vector2(0, 0), 1, 1, 1, display)
		player.healthBar = Physics.Bar(100, Color.red, 0, 0, 1, 1, 'left', display)
		player.takeDamage(1000, 1)
		self.assertEqual(player.state, 'Death')

	# Test if game gets characters
	def test_get_characters(self):
		characters = None
		try:
			characters = Proxy.getCharacters()
		except:
			pass
		self.assertIsNotNone(characters)

	# Test if game gets scenarios
	def test_get_scenarios(self):
		scenarios = None
		try:
			scenarios = Proxy.getScenarios()
		except:
			pass
		self.assertIsNotNone(scenarios)

	# Test if score is set
	def test_set_score(self):
		Proxy.setScore('TEST', 50)
		scores = Proxy.getScores()
		self.assertTrue(scores[len(scores) - 1]['name'] == 'TEST' and scores[len(scores) - 1]['score'] == 50)