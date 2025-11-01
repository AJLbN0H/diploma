from rest_framework.viewsets import ModelViewSet

from materials.models import Material, Section
from materials.serializer import MaterialSerializer, SectionSerializer


class SectionViewSet(ModelViewSet):
    """ViewSet модели Section."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class MaterialViewSet(ModelViewSet):
    """ViewSet модели Material."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
