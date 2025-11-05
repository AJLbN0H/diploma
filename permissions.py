from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Класс проверяющий, является ли пользователь администратором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Администраторы").exists()


class IsTeacher(BasePermission):
    """Класс проверяющий, является ли пользователь преподавателем"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Преподаватели").exists()


class IsStudent(BasePermission):
    """Класс проверяющий, является ли пользователь студентом"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Студенты").exists()


class IsOwner(BasePermission):
    """Класс проверяющий, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsStudentOwner(BasePermission):
    """Класс проверяющий, является ли студент владельцем"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.student:
            return True
        return False


class IsAdminOrTeacherOwner(BasePermission):
    """Класс проверяющий, что пользователь авторизован и состоит в группе администраторов или преподователей, а также проверяет, что преподователь является  владельцем."""

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
            return IsOwner().has_object_permission(request, view, obj)

        return False


class IsAdminOrTeacher(BasePermission):
    """Класс проверяющий, что пользователь авторизован и состоит в группе администраторов или преподователей."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_admin = IsAdmin().has_permission(request, view)
        is_teacher = IsTeacher().has_permission(request, view)

        return is_admin or is_teacher


class IsAdminOrStudentOwner(BasePermission):
    """Класс проверяющий, что пользователь авторизован и состоит в группе администраторов или студентов, a также является владельцем."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_admin = IsAdmin().has_permission(request, view)
        is_student = IsStudent().has_permission(request, view)

        return is_admin or is_student

    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True

        if IsStudent().has_permission(request, view):
            return IsStudentOwner().has_object_permission(request, view, obj)


class IsAdminOrStudent(BasePermission):
    """Класс проверяющий, что пользователь авторизован и состоит в группе администраторов или студентов."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_admin = IsAdmin().has_permission(request, view)
        is_student = IsStudent().has_permission(request, view)

        return is_admin or is_student
