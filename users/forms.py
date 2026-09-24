import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import forms

from users.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if email is None:
    #         raise forms.ValidationError(
    #             "Поле не может быть пустым."
    #         )
    #
    #     pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$'
    #     if re.fullmatch(pattern, email) == False:
    #         raise forms.ValidationError(
    #             "Некорректтный формат email."
    #         )
    #     return email
    #
    # def clean_num_phone(self):
    #     num_phone = self.cleaned_data["num_phone"]
    #     pattern = r'^(\+7|8)(\s|-|\()\d{3}(\s|-|\)|\)$'
    #     if re.match(pattern, num_phone) == False:
    #         raise forms.ValidationError(
    #             "Некорректный формат номера телефона."
    #         )
    #
    #     return num_phone

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for field in self.fields.values():
    #         field.widget.attrs["class"] = "form-control"


class LoginForm(AuthenticationForm):
    pass
