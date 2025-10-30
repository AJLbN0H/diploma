from django.db import models

from users.models import User


class Section(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Название раздела", help_text="Введите название раздела"
    )
    description = models.TextField(
        verbose_name="Описание раздела",
        blank=True,
        null=True,
        help_text="Введите описание раздела",
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец раздела",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздед"
        verbose_name_plural = "Разделы"


class Material(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Название материала", help_text="Введите название материала"
    )
    description = models.TextField(
        verbose_name="Описание материала",
        blank=True,
        null=True,
        help_text="Введите описание материала",
    )
    course = models.ForeignKey(
        Section,
        verbose_name="Курс",
        on_delete=models.SET_NULL,
        help_text="Выберите курс",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец материала",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"


