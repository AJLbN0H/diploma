from django.db import models

from materials.models import Material
from users.models import User


class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(
        verbose_name="Описание теста",
        blank=True,
        null=True,
    )
    material = models.ForeignKey(
        Material,
        verbose_name="Материал",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Создатель теста",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    passing_score = models.PositiveIntegerField(
        verbose_name="Минимальный бал для зачета"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"\nНазвание теста:{self.name}\nМинимальный бал для зачета: {self.passing_score}\n"

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):

    QUESTION_TYPE = [
        ("single", "один правильный"),
        ("multiple", "несколько правильных"),
        ("text", "текстовый ответ"),
    ]

    name = models.CharField(max_length=200, verbose_name="Название вопроса")
    text = models.TextField(
        verbose_name="Текст вопроса",
    )
    test = models.ForeignKey(
        Test,
        verbose_name="Тест",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    question_type = models.CharField(
        max_length=8,
        verbose_name="Варианты ответов",
        choices=QUESTION_TYPE,
        default="single",
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Создатель вопроса",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"\nНазвание вопроса:{self.name}\nТестирование: {self.test}\n"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    text = models.TextField(
        verbose_name="Ответ на вопрос",
    )
    question = models.ForeignKey(
        Question,
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    student = models.ForeignKey(
        User, verbose_name="Студент", blank=True, null=True, on_delete=models.CASCADE
    )
    is_correct = models.BooleanField(verbose_name="Правильность ответа", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"\nВопрос:{self.question}\nПравильность ответа: {self.is_correct}\n"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class TestResult(models.Model):
    student = models.ForeignKey(
        User, verbose_name="Студент", blank=True, null=True, on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, verbose_name="Вопрос", on_delete=models.CASCADE
    )
    answers = models.JSONField(verbose_name="Сохранение ответов студента в json файл")

    def __str__(self):
        return f"\nСтудент:{self.student}\nВопрос: {self.question}\n"

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
