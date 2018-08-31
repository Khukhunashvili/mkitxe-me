from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
	message = models.CharField(max_length=250)
	response = models.CharField(max_length=250, null=True)
	to = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateField(default=date.today)

	def save(self, *args, **kwargs):
	    models.Model.save(self, *args, **kwargs )
