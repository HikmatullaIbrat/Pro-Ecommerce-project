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



class LoginForm(forms.Form):

    user_name = forms.CharField( # making the input for full name
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'User Name'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
            }
        )
    )
    #password = forms.CharField()

class RegisterationForm(forms.Form):
    
    username = forms.CharField()
    email = forms.EmailField()
    
    password = forms.CharField(widget= forms.PasswordInput)
    password2 = forms.CharField(widget= forms.PasswordInput, label = 'Confirm Password')

    # for not registering two users with same name
    def clean_username(self):
        #User = get_user_model()
        username = self.cleaned_data.get('username')
        name = User.objects.filter(username = username)
        if name.exists():
            raise forms.ValidationError('username is take')
        return username

    # for not allowing two users registration with same email
    def clean_email(self):
        #User = get_user_model()
        email = self.cleaned_data.get('email')
        email_existance = User.objects.filter(email = email)
        if email_existance.exists():
            raise forms.ValidationError('Email is taken')

        return email


    # to check whether passwords matching with each other
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError('Password must match!')
        return data

 