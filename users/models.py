from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    username=models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя")
    email=models.CharField(max_length=200, unique=True, verbose_name="Почта пользователя")
    token=models.CharField(max_length=200, blank=True, null=True, verbose_name="Токен подтверждения")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name="пользователь"
        verbose_name_plural="пользователи"
        ordering=["email"]
        permissions = [("can_manage_users", "Can manage users")]

    def __str__(self):
        return self.username