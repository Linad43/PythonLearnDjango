from django.conf import settings
from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О.",
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"
        ordering = ["full_name"]


class Message(models.Model):
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема письма",
    )
    body = models.TextField(
        verbose_name="Тело письма",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    start_time = models.DateTimeField(
        verbose_name="Дата и время начала",
    )
    end_time = models.DateTimeField(
        verbose_name="Дата и время окончания",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("created", "Создана"),
            ("started", "Запущена"),
            ("finished", "Завершена"),
        ],
        default="created",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(
        Recipient,
        related_name="mailings",
        verbose_name="Получатели",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Владелец",
    )

    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = "created"
        elif now <= self.end_time:
            new_status = "started"
        else:
            new_status = "finished"

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])

    def __str__(self):
        return f"Рассылка №{self.pk}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["start_time"]


class MailingAttempt(models.Model):
    STATUS_SUCCESS = "Успешно"
    STATUS_FAILED = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILED, "Не успешно"),
    ]

    attempt_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время попытки",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
    )
    server_response = models.TextField(
        blank=True,
        verbose_name="Ответ почтового сервера",
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    def __str__(self):
        return f"{self.mailing} — {self.status}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылок"
        ordering = ["-attempt_time"]
