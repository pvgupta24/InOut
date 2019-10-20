from django.db import models
from django.contrib.auth.models import User


class Speech(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(blank=True, max_length=50)
	video = models.FileField(blank=True, null=True)
	audio = models.FileField(blank=True, null=True)
	manuscript = models.CharField(blank=True, null=True, max_length=500)
	speech2text = models.CharField(blank=True, null=True, max_length=500)