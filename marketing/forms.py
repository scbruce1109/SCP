from django import forms
from .models import MarketingPreference, Subscriber

class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Markeing Email?', required=False)
    class Meta:
        model = MarketingPreference
        fields = [
                'subscribed'
        ]


class SubscribeForm(forms.ModelForm):
    # email   = forms.EmailField()
    class Meta:
        model = Subscriber
        fields = [
            'name',
            'email'
        ]

        labels = {
            'name': '',
            'email': ''
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'})
        }
