from rest_framework.routers import SimpleRouter

from materials.views import SectionViewSet, MaterialViewSet

app_name = 'materials'

router = SimpleRouter()
router.register("section/", SectionViewSet)
router.register("material/", MaterialViewSet)

urlpatterns = [] + router.urls
