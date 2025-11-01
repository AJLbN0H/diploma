from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    ROLE = [
        ("admin", "Администратор"),
        ("teacher", "Преподователь"),
        ("student", "Студент"),
    ]

    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(
        upload_to="users/",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=7, verbose_name="Роль", choices=ROLE, default="student"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
