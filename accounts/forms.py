from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	"""
	This custom form lets the system
	integrate three more fields
	when creating a user.
	"""
	class Meta:
		model = CustomUser
		fields = ('username', 'age', 'email',)


class CustomUserChangeForm(UserChangeForm):
	"""
	This form gives an opportunity
	to change these three custom fields.
	"""
	class Meta:
		model = CustomUser
		fields = ('username', 'age', 'email',)