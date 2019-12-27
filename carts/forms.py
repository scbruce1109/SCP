from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse


class DiscountCodeForm(forms.Form):
    code       = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Discount Code', 'id': 'discount-input'}))
