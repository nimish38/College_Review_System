from django import forms
from django.forms import ModelForm,PasswordInput, Textarea ,CharField
from Reviews.models import Review
from django.contrib.auth.models import User


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [ 'rating', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 15})
        }
		
class UserForm(ModelForm):
	class Meta:
		model=User
		fields=['username', 'password']
		widgets={
			'password':forms.PasswordInput()
		}