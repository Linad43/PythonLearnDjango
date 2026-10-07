from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, ListView, CreateView, UpdateView, DeleteView

from .models import Mailing, Recipient, MailingAttempt
from .services import send_mailing


class OwnerQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(owner=self.request.user)


class MailingStatsView(LoginRequiredMixin, TemplateView):
    template_name = "stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        attempts = MailingAttempt.objects.filter(
            mailing__owner=self.request.user
        )

        context["successful_attempts"] = attempts.filter(
            status=MailingAttempt.STATUS_SUCCESS
        ).count()

        context["failed_attempts"] = attempts.filter(
            status=MailingAttempt.STATUS_FAILED
        ).count()

        context["sent_messages"] = context["successful_attempts"]

        return context


@method_decorator(cache_page(60), name="dispatch")
class MailingHomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cached_stats = cache.get("mailings_home_stats")

        if cached_stats is None:
            now = timezone.now()
            mailings = Mailing.objects.all()

            for mailing in mailings:
                mailing.update_status()

            cached_stats = {
                "mailings_count": mailings.count(),
                "active_mailings_count": mailings.filter(
                    start_time__lte=now,
                    end_time__gte=now,
                ).count(),
                "recipients_count": Recipient.objects.count(),
            }

            cache.set(
                "mailings_home_stats",
                cached_stats,
                60,
            )

        context.update(cached_stats)

        return context


class MailingSendView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing_send.html"
    context_object_name = "mailing"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            result = send_mailing(self.object)

            messages.success(
                request,
                f"Рассылка завершена. "
                f"Успешно: {result['success']}, "
                f"с ошибками: {result['failed']}.",
            )

        except ValueError as error:
            messages.error(request, str(error))

        return redirect(
            "mailings:mailing_send",
            pk=self.object.pk,
        )


class RecipientListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(
    LoginRequiredMixin,
    OwnerQuerysetMixin,
    UpdateView,
):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientDeleteView(
    LoginRequiredMixin,
    OwnerQuerysetMixin,
    DeleteView,
):
    model = Recipient
    template_name = "recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")
