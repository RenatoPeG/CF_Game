from django.contrib import admin
from . models import Character
from . models import Scenario

# Register your models here.
admin.site.register(Character)
admin.site.register(Scenario)