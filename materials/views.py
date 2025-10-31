from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)

from materials.models import Material, Section
from materials.serializer import MaterialSerializer, SectionSerializer


class SectionCreateAPIView(CreateAPIView):
    """Generic создания раздела."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SectionListAPIView(ListAPIView):
    """Generic списка разделов."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SectionRetrieveAPIView(ListAPIView):
    """Generic просмотра подробной информации о разделе."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SectionUpdateAPIView(UpdateAPIView):
    """Generic обновления ирформации раздела."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class SectionDestroyAPIView(DestroyAPIView):
    """Generic удаления раздела."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class MaterialCreateAPIView(CreateAPIView):
    """Generic создания материала."""

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
    """Generic обновления ирформации материала."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialDestroyAPIView(DestroyAPIView):
    """Generic удаления материала."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
