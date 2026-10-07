from django.urls import path

from .apps import MailingsConfig
from .views import MailingSendView, MailingHomeView, MailingStatsView, RecipientListView, RecipientCreateView, \
    RecipientUpdateView, RecipientDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path("", MailingHomeView.as_view(), name="home"),

    path("stats/", MailingStatsView.as_view(), name="stats"),

    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipients/create/",
        RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipients/<int:pk>/edit/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),

    path(
        "<int:pk>/send/",
        MailingSendView.as_view(),
        name="mailing_send",
    ),
]
