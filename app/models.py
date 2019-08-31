from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pet(models.Model):
	name = models.CharField(max_length=50)
	age = models.IntegerField()
	available = models.BooleanField(default=True)
	Image = models.ImageField()
	price = models.FloatField()
	last_update = models.DateTimeField(auto_now=True) 

	def __str__(self):
		return self.name

	def my_boolean_field(self, obj):
		return obj.available == 'available'
		my_boolean_field.boolean = True