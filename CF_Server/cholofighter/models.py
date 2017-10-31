from django.db import models

# Create your models here.
class Character(models.Model):
	character_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	asset_prefix = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Scenario(models.Model):
	scenario_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	asset_prefix = models.CharField(max_length=100)

	def __str__(self):
		return self.name