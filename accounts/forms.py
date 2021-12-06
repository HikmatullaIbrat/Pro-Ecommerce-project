from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField


User = get_user_model()

# this code is for adding custom user model and admin
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label= 'Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        # so after the creating a required field full_name we can add that field to forms
        # fields = ('email',)
        fields = ('email','full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=  password2:
            raise forms.ValidationError("Password don't match")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user 


class UserAdminChangeForm(forms.ModelForm):
    
    """ A form for updating users. Includes all the fields on the user, but replaces the password field
    with admin's password hash display field. """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        # fields = ('email', 'password', 'active', 'admin')
        fields = ('full_name','email', 'password', 'active', 'admin')

    def clean_password(self):
        """Regardless of what the user provides, return the initial value. This is done here, rather    
        than on the field, because the field doesn't have access to the initial value.   """
        return self.initial["password"]

             
# this portion is also used if don't have custom user model
class GuestForm(forms.Form):
     email = forms.EmailField(
         widget=forms.EmailInput(
             attrs={
                'class': 'form-control col-12 col-lg-6',
                'placeholder': 'Guest Email'
            }
        )
    )

class LoginForm(forms.Form):

    email = forms.EmailField( # making the input for full name
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-12 col-lg-6',
                'placeholder': 'User Name'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control col-12 col-lg-6',
            'placeholder': 'Password'
            }
        )
    )
    #password = forms.CharField()

# form after creating custom user model
class RegisterationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label= 'Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        # so after the creating a required field full_name we can add that field to forms
        # fields = ('email',)
        fields = ('email','full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=  password2:
            raise forms.ValidationError("Password don't match")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.active = False  # Send confirmation email to check email exists or not, if active can log in
        if commit:
            user.save()
        return user 

# the first registration form
# class RegisterationForm(forms.Form):
    
#     username = forms.CharField()
#     email = forms.EmailField()
    
#     password = forms.CharField(widget= forms.PasswordInput)
#     password2 = forms.CharField(widget= forms.PasswordInput, label = 'Confirm Password')

#     # for not registering two users with same name
#     def clean_username(self):
#         #User = get_user_model()
#         username = self.cleaned_data.get('username')
#         name = User.objects.filter(username = username)
#         if name.exists():
#             raise forms.ValidationError('username is take')
#         return username

#     # for not allowing two users registration with same email
#     def clean_email(self):
#         #User = get_user_model()
#         email = self.cleaned_data.get('email')
#         email_existance = User.objects.filter(email = email)
#         if email_existance.exists():
#             raise forms.ValidationError('Email is taken')

#         return email


#     # to check whether passwords matching with each other
#     def clean(self):
#         data = self.cleaned_data
#         password = self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')
#         if password2 != password:
#             raise forms.ValidationError('Password must match!')
#         return data
