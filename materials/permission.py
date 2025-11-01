from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Класс проверящий является ли пользователь администратором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Администраторы").exists()


class IsTeacher(BasePermission):
    """Класс проверящий является ли пользователь преподователем"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Преподователи").exists()


class IsStudent(BasePermission):
    """Класс проверящий является ли пользователья стуеднтом"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Студенты").exists()


class IsOwner(BasePermission):
    """Класс проверящий является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False