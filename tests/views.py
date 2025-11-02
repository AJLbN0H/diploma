from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from permissions import (
    IsAdminOrTeacher,
    IsAdminOrTeacherOwner,
    IsAdminOrStudent,
    IsAdminOrStudentOwner,
    IsStudentOwner,
)

from tests.models import Test, Question, Answer, TestResult
from tests.serializer import (
    TestSerializer,
    QuestionSerializer,
    AnswerSerializer,
    TestResultSerializer,
    TestDetailSerializer,
    TestSubmissionSerializer,
)
from tests.services import TestCalculateService


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


class TestDetailAPIView(RetrieveAPIView):
    """Получение теста для прохождения."""

    permission_classes = [IsAuthenticated]
    serializer_class = TestDetailSerializer
    queryset = Test.objects.all()


class TestSubmitView(APIView):
    """Отправка ответов на тест."""

    permission_classes = [IsAuthenticated]

    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        serializer = TestSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        result_data = TestCalculateService.calculate_results(
            self, test, serializer.validated_data["answers"]
        )

        test_result = TestResult.objects.create(
            student=request.user,
            test=test,
            score=result_data["score"],
            total_questions=result_data["total_questions"],
            correct_answers=result_data["correct_answers"],
            percentage=result_data["percentage"],
            is_passed=result_data["is_passed"],
            answers_data=serializer.validated_data["answers"],
        )

        return Response(result_data, status=201)


class TestResultListAPIView(ListAPIView):
    """Generic получения списка результатов тестов пользователя."""

    permission_classes = [IsAuthenticated]
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.all()


class TestResultRetrieveAPIView(RetrieveAPIView):
    """Generic получения детальной информации о результате теста."""

    permission_classes = [IsAuthenticated]
    serializer_class = TestResultSerializer
    queryset = TestResult.objects.all()

    def get_queryset(self):
        return TestResult.objects.filter(student=self.request.user)


class TestResultDestroyAPIView(DestroyAPIView):
    """Generic удаления результата теста."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [(IsAdminOrTeacher | IsStudentOwner) & IsAuthenticated]
