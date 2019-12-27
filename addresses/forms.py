from django import forms

from.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code',
        ]

        labels = {
            'address_line_1': '',
            'address_line_2': '',
            'city': '',
            'country': '',
            'state': '',
            'postal_code': '',
        }

        widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address Line 1', 'class': 'input-long'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
        }
