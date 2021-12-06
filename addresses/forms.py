from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    # this meta classes are used when we use the builtain form of Django with our own page
    class Meta:
        model = Address
        fields=[
            #    'billing_profile',
            #    'address_type',
               'address_line_1',
               'address_line_2',
               'city',
               'country',
               'province',
               'postal_code',
        ]