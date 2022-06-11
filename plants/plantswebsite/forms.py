from django import forms
from django.forms import fields
from .models import ContactProfile

class ContactProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(max_length=254,required=True)
    message = forms.CharField(max_length=1000,required=True)

    class Meta:
        model = ContactProfile
        fields = ('name','email','message',)