from rest_framework import serializers

from materials.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Material."""

    class Meta:
        model = Material
        fields = "__all__"
