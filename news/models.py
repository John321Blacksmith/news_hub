from django.db import models
from django.urls import reverse
# Create your models here.


class News(models.Model):
	"""
	This model represens a single
	news entity with the necessary
	fields.
	"""
	title = models.CharField(max_length=255)
	date = models.DateTimeField()
	source = models.URLField(max_length=255)
	content = models.TextField()
	image = models.URLField(max_length=255)
	category = models.CharField(max_length=150, blank=True)

	def __str__(self):
		return self.title[:47] + '...'

	def get_absolute_url(self):
		return reverse('news:news_details', kwargs={'pk': self.pk})