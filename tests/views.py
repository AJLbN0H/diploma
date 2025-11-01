from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.viewsets import ViewSet

from tests.models import Test, Question, Answer, TestResult
from tests.serializer import (
    TestSerializer,
    QuestionSerializer,
    AnswerSerializer,
    TestResultSerializer,
)


class TestViewSet(ViewSet):
    """ViewSet модели Test."""

    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionViewSet(ViewSet):
    """ViewSet модели Question."""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(ViewSet):
    """ViewSet модели Answer."""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class TestResultCreateAPIView(CreateAPIView):
    """Generic создания результата теста."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer


class TestResultListAPIView(ListAPIView):
    """Generic списка результата тестов."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer


class TestResultRetrieveAPIView(RetrieveAPIView):
    """Generic списка результата тестов."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer


class TestResultDestroyAPIView(DestroyAPIView):
    """Generic удаления результата теста."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
