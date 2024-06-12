from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import Author


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    
    class Meta:
        model = Author
        fields = [
            'user_name', 'email', 'avatar', 'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        validate_password(password)
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'Password dot match')
        return cleaned_data
