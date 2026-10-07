from django.urls import path

from .apps import UsersConfig
from .views import CustomLoginView, CustomLogoutView, ConfirmEmailView, RegistrationView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('register/', RegistrationView.as_view(), name='register'),
    path(
        "confirm/<int:user_id>/", ConfirmEmailView.as_view(), name="confirm_email", ),
]
