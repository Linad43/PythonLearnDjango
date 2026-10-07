from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView

from users.forms import RegistrationForm, LoginForm
from .models import User


class ConfirmEmailView(View):

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        user.is_active = True
        user.save(update_fields=["is_active"])

        messages.success(
            request,
            "Email успешно подтверждён. Теперь вы можете войти.",
        )

        return redirect("users:login")


class RegistrationView(FormView):
    # template_name = "users/register.html"
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = "/users/login/"

    def form_valid(self, form):
        user = form.save()

        confirmation_url = self.request.build_absolute_uri(
            reverse(
                "users:confirm_email",
                kwargs={"user_id": user.pk},
            )
        )

        send_mail(
            subject="Подтверждение регистрации",
            message=(
                f"Здравствуйте!\n\n"
                f"Для подтверждения регистрации перейдите по ссылке:\n"
                f"{confirmation_url}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        messages.success(
            self.request,
            "Регистрация завершена. "
            "Проверьте электронную почту для подтверждения.",
        )

        return redirect(self.success_url)


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Шаблон для отображения формы входа
    authentication_form = LoginForm
    success_url = reverse_lazy('catalog:home')  # URL для перенаправления после успешного входа


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('goodbye')  # URL для перенаправления после выхода из системы


# class RegisterView(CreateView):
#     form_class = RegistrationForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('catalog:home')
