from django import forms
from django.forms import ModelForm,PasswordInput, Textarea ,CharField
from Reviews.models import Review,AnsweredQueries
from django.contrib.auth.models import User
#from College.models import College


class ReviewForm(ModelForm):
    anonymous=forms.BooleanField(required =False)
    class Meta:
        model = Review
        fields = ['anonymous' , 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 15})
        }


class UserForm(ModelForm):
	college_name=forms.CharField(max_length=100)
	class Meta:
		model=User
		fields=['username','college_name','password']
		widgets={
			'password':forms.PasswordInput()
		}
