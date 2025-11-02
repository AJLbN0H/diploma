from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from permissions import (
    IsAdminOrTeacher,
    IsAdminOrTeacherOwner,
    IsAdminOrStudent,
    IsAdminOrStudentOwner,
)
from tests.models import Test, Question, Answer, TestResult
from tests.serializer import (
    TestSerializer,
    QuestionSerializer,
    AnswerSerializer,
    TestResultSerializer,
)


class TestViewSet(ModelViewSet):
    """ViewSet модели Test."""

    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_permissions(self):
        """Метод проверки прав доступа."""

        if self.action == "create":
            self.permission_classes = [IsAdminOrTeacher]
        elif self.action == "list":
            self.permission_classes = [IsAdminOrTeacher]
        elif self.action in ["partial_update", "update", "retrieve"]:
            self.permission_classes = [IsAdminOrTeacherOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAdminOrTeacherOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле owner на текущего авторизованного пользователя."""

        serializer.save(owner=self.request.user)


class QuestionViewSet(ModelViewSet):
    """ViewSet модели Question."""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        """Метод проверки прав доступа."""

        if self.action == "create":
            self.permission_classes = [IsAdminOrTeacher]
        elif self.action == "list":
            self.permission_classes = [IsAdminOrTeacher]
        elif self.action in ["partial_update", "update", "retrieve"]:
            self.permission_classes = [IsAdminOrTeacherOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAdminOrTeacherOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле owner на текущего авторизованного пользователя."""

        serializer.save(owner=self.request.user)


class AnswerViewSet(ModelViewSet):
    """ViewSet модели Answer."""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_permissions(self):
        """Метод проверки прав доступа."""

        if self.action == "create":
            self.permission_classes = [IsAdminOrStudent]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["partial_update", "update", "retrieve"]:
            self.permission_classes = [IsAdminOrStudentOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAdminOrStudentOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле student на текущего авторизованного пользователя."""

        serializer.save(student=self.request.user)


class TestResultListAPIView(ListAPIView):
    """Generic списка результата тестов."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]


class TestResultRetrieveAPIView(RetrieveAPIView):
    """Generic просмотра подробной информации о тесте."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAdminOrStudentOwner]


class TestResultDestroyAPIView(DestroyAPIView):
    """Generic удаления результата теста."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAdminOrStudentOwner]
