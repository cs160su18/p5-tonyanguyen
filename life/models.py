from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
	name = models.CharField(max_length=50)
	cost = models.PositiveSmallIntegerField()
	quantity = models.PositiveSmallIntegerField()
	
	def __str__(self):
		return self.name
	
	def in_stock(self):
		return self.quantity > 0

class Cart(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.PositiveSmallIntegerField()
	