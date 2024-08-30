from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

class OTPForm(forms.Form):
    combined_otp = forms.CharField(max_length=6)

class LoginForm(forms.Form):
    identifier = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
