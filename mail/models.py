from django.db import models

# Create your models here.
from django.core.validators import FileExtensionValidator
from django.db import models
from users.models import User


class Recipient(models.Model):
    email=models.CharField(max_length=100, unique=True, verbose_name="Почта")
    full_name=models.CharField(max_length=300, blank=True, null=True, verbose_name="Ф.И.О.")
    comment=models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "получатель письма"
        verbose_name_plural = "получатели письма"
        ordering=["email"]
        permissions = [("can_manage_recipient","Can manage recipient")]



class Letter(models.Model):
    subject=models.CharField(max_length=100, verbose_name="Тема письма")
    letter_body=models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering=["subject"]

class Mailing(models.Model):

    STATUS_CHOICES = (
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    )

    first_send=models.DateTimeField(verbose_name="Время запуска",  blank=True, null=True)
    end_send=models.DateTimeField(verbose_name="Время завершения",  blank=True, null=True)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    letter=models.ForeignKey(Letter, on_delete=models.CASCADE, verbose_name="Письмо")
    recipients=models.ManyToManyField(Recipient, verbose_name="Получатель")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return f'Рассылка "{self.letter.subject}"'

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["pk"]
        permissions = [("can_manage_mailing", "Can manage mailing")]


class MailingTry(models.Model):
    STATUS_SUCCESS = "success"
    STATUS_DEFEAT = "defeat"
    STATUS_CHOICES = (
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_DEFEAT, "Не успешно"),
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, verbose_name="Статус рассылки")
    smtp_response = models.TextField(verbose_name="Ответ ошибки SMTP-сервера")

    def __str__(self):
        return f"{self.mailing}_{self.create_at}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["mailing", "create_at"]







