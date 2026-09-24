from django.urls import path

from .apps import UsersConfig
from .views import RegisterView, CustomLoginView, CustomLogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
