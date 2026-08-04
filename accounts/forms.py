from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomerRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone',
            'password1',
            'password2'
    ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Mobile Number'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control'
        })

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "This email is already registered."
            )

        return email


class SellerRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Mobile Number'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control'
        })

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "This email is already registered."
            )

        return email


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
            "profile_image",
        ]

        widgets = {

            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "pincode": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "profile_image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }