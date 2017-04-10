from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    """Displayed when creating profile."""
    # Had to create a new form for the email, as the user.email was not required
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
        }


