from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)

from materials.models import Material
from materials.serializer import MaterialSerializer


class MaterialCreateAPIView(CreateAPIView):
    """Generic создания материалов."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialListAPIView(ListAPIView):
    """Generic списка материалов."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialRetrieveAPIView(ListAPIView):
    """Generic просмотра подробной информации о материале."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialUpdateAPIView(UpdateAPIView):
    """Generic обновления ирформации материалов."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialDestroyAPIView(DestroyAPIView):
    """Generic удаления материалов."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
