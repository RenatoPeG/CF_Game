from rest_framework import serializers
from . models import Character
from . models import Scenario

class CharacterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Character
		fields = ('character_id', 'name', 'asset_prefix')

class ScenarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Scenario
		fields = ('scenario_id', 'name', 'asset_prefix')