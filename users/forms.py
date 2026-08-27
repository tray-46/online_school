from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm as DefaultUserCreationForm
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class RegisterForm(UserCreationForm):
    """ """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)


class UserChangeForm(DefaultUserCreationForm):
    """ """

    class Meta(DefaultUserCreationForm.Meta):
        model = User
