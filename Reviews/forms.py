from django import forms
from django.forms import ModelForm,PasswordInput, Textarea ,CharField
from Reviews.models import Review,StudentUser, IndustryUser
from django.contrib.auth.models import User


class ReviewForm(ModelForm):
    anonymous = forms.BooleanField(required =False)
    class Meta:
        model = Review
        fields = ['anonymous', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 15})
        }


class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class StudUserForm(ModelForm):
    class Meta:
        model = StudentUser
        fields = ['category', 'college']


class IndUserForm(ModelForm):
    class Meta:
        model = IndustryUser
        fields = ['company']
