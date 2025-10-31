from rest_framework.viewsets import ViewSet

from materials.models import Material, Section
from materials.serializer import MaterialSerializer, SectionSerializer


class SectionViewSet(ViewSet):
    """ViewSet модели Section."""

    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class MaterialViewSet(ViewSet):
    """ViewSet модели Material."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

