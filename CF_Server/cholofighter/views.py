from django.shortcuts import render
from rest_framework import viewsets
from . models import Character
from . models import Scenario
from . serializers import CharacterSerializer
from . serializers import ScenarioSerializer

# Create your views here.
class CharacterViewSet(viewsets.ModelViewSet):
	queryset = Character.objects.all()
	serializer_class = CharacterSerializer

class ScenarioViewSet(viewsets.ModelViewSet):
	queryset = Scenario.objects.all()
	serializer_class = ScenarioSerializer