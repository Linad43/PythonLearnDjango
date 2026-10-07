from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import MailingAttempt


def send_mailing(mailing):
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError("Рассылка сейчас недоступна для отправки")

    recipients = mailing.recipients.all()

    success_count = 0
    failed_count = 0

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
            )

            MailingAttempt.objects.create(
                mailing=mailing,
                status="Успешно",
            )

            success_count += 1

        except Exception as error:
            MailingAttempt.objects.create(
                mailing=mailing,
                status="Не успешно",
                server_response=str(error),
            )

            failed_count += 1

    return {
        "success": success_count,
        "failed": failed_count,
    }