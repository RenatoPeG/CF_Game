from django.shortcuts import render
from rest_framework import viewsets
from . models import Character
from . models import Scenario
from . models import Score
from . serializers import CharacterSerializer
from . serializers import ScenarioSerializer
from . serializers import ScoreSerializer

# Create your views here.
class CharacterViewSet(viewsets.ModelViewSet):
	queryset = Character.objects.all()
	serializer_class = CharacterSerializer

class ScenarioViewSet(viewsets.ModelViewSet):
	queryset = Scenario.objects.all()
	serializer_class = ScenarioSerializer

class ScoreViewSet(viewsets.ModelViewSet):
	queryset = Score.objects.all()
	serializer_class = ScoreSerializer