from django import forms
from django.contrib.auth import authenticate

from .models import *


class LoginUserForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Username:'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password:'
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(LoginUserForm, self).clean(*args, **kwargs)


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Username:'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password:'
    }))

    full_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Your Name:'
    }))

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'full_name'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(RegisterUserForm, self).clean(*args, **kwargs)


class PostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': 'Title:'
    }))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': "What's on your mind?"
    }))

    class Meta:
        model = Post
        fields = [
            'title',
            'body'
        ]



