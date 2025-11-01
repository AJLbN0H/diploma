from rest_framework import serializers

from materials.models import Material, Section


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer модели Material."""

    class Meta:
        model = Material
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    """Serializer модели Section."""

    class Meta:
        model = Section
        fields = "__all__"
