from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class UpdatePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})
