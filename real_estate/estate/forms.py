from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms. ModelForm):
    username=forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username','email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        # Check if the passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data