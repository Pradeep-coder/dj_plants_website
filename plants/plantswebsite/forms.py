from django import forms
from django.forms import fields
from .models import ContactProfile, User
from django.contrib.auth.forms import UserCreationForm

class ContactProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(max_length=254,required=True)
    message = forms.CharField(max_length=1000,required=True)

    class Meta:
        model = ContactProfile
        fields = ('name','email','message',)

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"contact__input"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"contact__input"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"contact__input"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"contact__input"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
