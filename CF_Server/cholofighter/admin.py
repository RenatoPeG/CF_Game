from django.contrib import admin
from . models import Character
from . models import Scenario
from . models import Score

# Register your models here.
admin.site.register(Character)
admin.site.register(Scenario)
admin.site.register(Score)