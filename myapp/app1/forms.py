from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from.models import worker, Owner_work


class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	username = forms.CharField(label=("Mobile Number/Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			 'last_name',
			 'email',
		]

class UpdateUserDetailForm(forms.ModelForm):
	class Meta:
		model = worker
		fields = [

			'age',
			'city',
			'Type_of_work',
			'address',
             'status',
			'contact',
			'charge_per_day',
			'resume',
			'profile_pic',
			'twt',
			'fb',
			'insta',

		]

class OwnerRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	username = forms.CharField(label=("Mobile Number/Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2']



# forms.py

from django import forms
from .models import Owner_work

class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Owner_work
        fields = ['person_name', 'work_dec', 'work_type', 'time', 'place', 'pay_for_work']


# forms.py (Delete form not needed as we don't require any input for deleting)
# This is here for consistency purposes.

from django import forms
from .models import Owner_work

class JobDeleteForm(forms.ModelForm):
    class Meta:
        model = Owner_work
        fields = []


from django import forms
from .models import Owner_work

# class OwnerWorkForm(forms.ModelForm):
#     class Meta:
#         model = Owner_work
#         fields = ['person_name', 'work_dec', 'work_type', 'time', 'place', 'pay_for_work']
class OwnerWorkForm(forms.ModelForm):
    class Meta:
        model = Owner_work
        fields = ['person_name', 'work_dec', 'work_type', 'time', 'place', 'pay_for_work', 'experience_level', 'vacancies', 'applicants_needed', 'deadline']

######contactfrom django import forms
from .models import ClientTestimonial
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = ClientTestimonial
        fields = ['name', 'company', 'image', 'testimonial_text']
