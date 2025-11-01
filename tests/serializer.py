from rest_framework import serializers

from tests.models import Test, Question, Answer, TestResult


class TestSerializer(serializers.ModelSerializer):
    """Serializer модели Test."""

    class Meta:
        model = Test
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer модели Question."""

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer модели Answer."""

    class Meta:
        model = Answer
        fields = ("text", "question")


class TestResultSerializer(serializers.ModelSerializer):
    """Serializer модели TestResult."""

    class Meta:
        model = TestResult
        fields = "__all__"
