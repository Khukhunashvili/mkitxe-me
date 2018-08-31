from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_email(email):
	if '.' not in email.split('@')[1]:
		raise ValidationError(
			_('მაილის ფორმატი არასწორია')
		)
	try:
		user = User.objects.get(email=email)
		if user is not None:
			raise ValidationError(
	            _('მოცემული იმეილი უკვე გამოყენებულია!')
	        )
	except User.DoesNotExist:
		pass

def validate_username(username):
	links = ('dashboard', 'comment', 'join', 'login', 'admin')
	try:
		user = User.objects.get(username=username)
		if user is not None:
			raise ValidationError(
				_('მოცემული მომხმარებლის სახელი უკვე გამოყენებულია!')
			)
	except User.DoesNotExist:
		pass

	if username in links:
		raise ValidationError(
				_('მოცემული მომხმარებლის სახელით რეგისტრაცია შეუძლებელია!')
			)


class RegistrationForm(forms.ModelForm):
	image = forms.ImageField(label='პროფილის სურათი')
	first_name = forms.CharField(label='სახელი')
	last_name = forms.CharField(label='გვარი')
	email = forms.EmailField(label='მეილი', validators=[validate_email])
	username = forms.CharField(validators=[validate_username], label='მომხმარებლის სახელი')
	password = forms.CharField(widget=forms.PasswordInput, label='პაროლი')

	class Meta:
		model = User
		fields = ['image', 'first_name','last_name', 'username', 'email', 'password']
		labels = {
				'username'   : 'მომხმარებლის სახელი',
				'email'      : 'მეილი',
				'password'   : 'პაროლი'
		}
		help_texts = {
				'username'   : None
		}
	def __init__(self, *args, **kwargs):
	    super(RegistrationForm, self).__init__(*args, **kwargs)

	    for key in self.fields:
	        self.fields[key].required = True
	    self.fields['image'].required = False


class LoginForm(forms.Form):
	username = forms.CharField(label='მომხმარებლის სახელი')
	password = forms.CharField(label='პაროლი', widget=forms.PasswordInput)
