from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import Form, PasswordInput


class PasswordForm(forms.Form):
    password = forms.CharField(label='', widget=PasswordInput())
    password_confirm = forms.CharField(label='', widget=PasswordInput())