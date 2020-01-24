from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    name = forms.CharField(
            label='',
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "Your name"
                    }
                    )
            )
    email = forms.EmailField(
            label='',
            widget=forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": "Your email"
                    }
                )
            )

    subject = forms.CharField(
            label='',
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "Subject"
                    }
                    )
            )

    content = forms.CharField(
            label='',
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": "Your message"
                    }
                )
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if not "gmail.com" in email:
        #     raise forms.ValidationError("Email has to be gmail.com")
        return email

    # def clean_content(self):
    #     raise forms.ValidationError("Ayy yoo bihh")
