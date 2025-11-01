from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Material, Section
from permissions import (
    IsAdminOrTeacherOwner,
    IsAdminOrTeacher,
)
from materials.serializer import MaterialSerializer, SectionSerializer


class SectionViewSet(ModelViewSet):
    """ViewSet модели Section."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_permissions(self):
        """Метод проверки прав доступа."""

        if self.action == "create":
            self.permission_classes = [IsAdminOrTeacher]
        if self.action == "list":
            self.permission_classes = [IsAdminOrTeacher]
        elif self.action in ["partial_update", "update", "retrieve"]:
            self.permission_classes = [IsAdminOrTeacherOwner]
        if self.action == "destroy":
            self.permission_classes = [IsAdminOrTeacherOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле owner на текущего авторизованного пользователя."""

        serializer.save(owner=self.request.user)


class MaterialViewSet(ModelViewSet):
    """ViewSet модели Material."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get_permissions(self):
        """Метод проверки прав доступа."""

        if self.action == "create":
            self.permission_classes = [IsAdminOrTeacher]
        if self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["partial_update", "update", "retrieve"]:
            self.permission_classes = [IsAdminOrTeacherOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAdminOrTeacherOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле owner на текущего авторизованного пользователя."""

        serializer.save(owner=self.request.user)
