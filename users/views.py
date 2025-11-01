from django.contrib.auth.models import Group
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializer import UserSerializer


class UserCreateApiView(CreateAPIView):
    """Generic создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод активацирующий пользователя при его создании и проверяющий в какую группу он входит."""

        user = serializer.save(is_active=True)
        user.set_password(user.password)

        if user.role == 'admin':
            group = Group.objects.get_or_create(name='Администраторы')
            user.groups.add(group)
        elif user.role == 'teacher':
            group = Group.objects.get_or_create(name='Преподователи')
            user.groups.add(group)
        elif user.role == 'student':
            group = Group.objects.get_or_create(name='Студенты')
            user.groups.add(group)

        user.save()