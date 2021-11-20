from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import get_user_model

User = get_user_model()
class ContactForm(forms.Form):
    full_name = forms.CharField( # making the input for full name
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your full Name'
            }
        )
    )

    email = forms.EmailField(       # making the email input field
        widget= forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Your email'
            }
        )
    )

    Message = forms.CharField( # making textarea for message by Django's form
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'Your message'
            }
        )
    )

    # and if we want to have our own validation so we write:   clean_input_type

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:     # email has to be gmail type
            raise forms.ValidationError('Email has to be gmail.com')
        return email




 