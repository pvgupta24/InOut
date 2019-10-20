from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import slugify


def generateUUID():
    return str(uuid4())


class Speech(models.Model):
	name = models.CharField(blank=True, max_length=50, unique=True)
	slug = models.SlugField(unique=True, default=generateUUID)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	video = models.FileField(blank=True, null=True)
	audio = models.FileField(blank=True, null=True)
	manuscript = models.CharField(blank=True, null=True, max_length=500)
	speech2text = models.CharField(blank=True, null=True, max_length=500)

	def save(self, *args, **kwargs):
		self.slug = slugify.slugify(self.name)
		super(Speech, self).save(*args, **kwargs)