from rest_framework.generics import CreateAPIView

from materials.models import Material
from materials.serializer import MaterialSerializer


class MaterialCreateApiView(CreateAPIView):
    """Generic создания материалов."""

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
