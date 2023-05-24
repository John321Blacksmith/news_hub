from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
	"""
	This custom user model adds one more
	useful field to the user info.
	"""
	age = models.PositiveIntegerField(null=True, blank=True)