from django.db import models

from users.models import User


class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название раздела")
    description = models.TextField(
        verbose_name="Описание раздела",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец раздела",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"\nНазвание раздела:{self.name}\n"

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


class Material(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название материала")
    description = models.TextField(
        verbose_name="Описание материала",
        blank=True,
        null=True,
    )
    section = models.ForeignKey(
        Section,
        verbose_name="Раздел",
        on_delete=models.CASCADE,
        default=None
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец материала",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"\nНазвание материала:{self.name}\nРаздел: {self.section}\n"

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
