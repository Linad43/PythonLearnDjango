from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Пароли не совпадают."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(
            self.cleaned_data["password"]
        )

        user.is_active = False

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    pass
