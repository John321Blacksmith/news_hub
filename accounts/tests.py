from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse


# Create your tests here.

class SignUpTest(TestCase):
	"""
	These tests check the work of the
	signup system.
	"""
	def test_url_exists_at_correct_loc(self):
		"""
		This test checks if the
		the url works in a common way.
		"""
		response = self.client.get('/accounts/signup/')
		self.assertEqual(response.status_code, 200)

	def test_url_available_via_name(self):
		"""
		This test checks if the url
		is available through the pattern name.
		"""
		response = self.client.get(reverse('signup'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'registration/signup.html')

	def test_signup_form(self):
		"""
		This test checks the work
		of the rendered form.
		"""
		response = self.client.post(
				reverse('signup'),
				{
					'username': 'TestUser',
					'email': 'test@mail.com',
					'password1': '1234hghdsfahgeywegje64fhjkdhzahgsf',
					'password2': '1234hghdsfahgeywegje64fhjkdhzahgsf',
				},
			)
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(get_user_model().objects.all().count(), 1)
		self.assertEqual(get_user_model().objects.all()[0].username, 'TestUser')
		self.assertEqual(get_user_model().objects.all()[0].email, 'test@mail.com')
