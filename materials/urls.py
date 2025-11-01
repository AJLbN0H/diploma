from django.urls import include, path
from rest_framework.routers import SimpleRouter

from materials.views import SectionViewSet, MaterialViewSet

app_name = "materials"

router = SimpleRouter()
router.register("section", viewset=SectionViewSet, basename="section")
router.register("material", viewset=MaterialViewSet, basename="material")

urlpatterns = [path("", include(router.urls))]
