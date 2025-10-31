from django.urls import path

from materials.views import SectionViewSet, MaterialViewSet

urlpatterns = [
    path("section/", SectionViewSet.as_view(), name="section"),
    path("material/", MaterialViewSet.as_view(), name="material"),
]
