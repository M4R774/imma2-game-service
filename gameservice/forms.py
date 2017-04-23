from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game

# Form that is used to sign up new users, extra fields are email and developer
# status

class SignUpForm(UserCreationForm):  # forms.ModelForm
    """Displayed when creating profile."""
    # Had to create a new form for the email, as the user.email was not required
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'autocomplete': 'off', 'class': 'form-control'}))
    applyAsDeveloper = forms.NullBooleanField(label="Apply as Developer", widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'password': forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
            # 'developer': forms.BooleanField()
        }

# Form that is used to add a new game

class AddGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'description', 'url', 'price')
