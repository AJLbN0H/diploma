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


class IsAdminOrTeacherOwner(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_admin = IsAdmin().has_permission(request, view)
        is_teacher = IsTeacher().has_permission(request, view)

        return is_admin or is_teacher

    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True

        if IsTeacher().has_permission(request, view):
            print(IsOwner().has_object_permission(request, view, obj))
            return IsOwner().has_object_permission(request, view, obj)

        return False


class IsAdminOrTeacher(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_admin = IsAdmin().has_permission(request, view)
        is_teacher = IsTeacher().has_permission(request, view)

        return is_admin or is_teacher


class IsAdminOrTeacherOrStudent(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_admin = IsAdmin().has_permission(request, view)
        is_teacher = IsTeacher().has_permission(request, view)
        is_student = IsStudent().has_permission(request, view)

        return is_admin or is_teacher or is_student
