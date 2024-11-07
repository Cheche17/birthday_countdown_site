from django import forms
from django.contrib.auth.models import User
from .models import GiftCountdown

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        user.is_staff = False  # Ensure the user is not an admin
        user.is_superuser = False  # Hash the password
        if commit:
            user.save()
        return user

class GiftForm(forms.ModelForm):
    countdown_date = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"])  # Moved to the correct indentation

    class Meta:
        model = GiftCountdown
        fields = ['gift_name', 'gift_description', 'countdown_date', 'recipient','image', 'video']
