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
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address 1', 'class': 'input-field full'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address 2', 'class': 'input-field full'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'input-field third'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'input-field full'}),
            'state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'input-field short'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code', 'class': 'input-field third'}),
        }
