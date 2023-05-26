from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


# Create your tests here.

class SignUpTest(TestCase):
	"""
	These tests check the work of the
	signup system.
	"""


	def test_model_data(self):
		"""
		This test checks if the model
		system works well.
		"""
		pass

	def test_url_exists_at_correct_loc(self):
		"""
		This test checks if the
		the url works in a common way.
		"""
		pass

	def test_url_available_via_name(self):
		"""
		This test checks if the url
		is available through the pattern name.
		"""
		pass

	def test_signup_page(self):
		"""
		This test checks the work
		of the rendered template.
		"""