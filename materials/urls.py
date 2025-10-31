from django.urls import path

from materials.views import (
    SectionCreateAPIView,
    SectionListAPIView,
    SectionRetrieveAPIView,
    SectionUpdateAPIView,
    SectionDestroyAPIView,
    MaterialCreateAPIView,
    MaterialListAPIView,
    MaterialRetrieveAPIView,
    MaterialUpdateAPIView,
    MaterialDestroyAPIView,
)

urlpatterns = [
    path("section/create/", SectionCreateAPIView.as_view(), name="section_create"),
    path("section/list/", SectionListAPIView.as_view(), name="section_list"),
    path("section/detail/", SectionRetrieveAPIView.as_view(), name="section_detail"),
    path("section/update/", SectionUpdateAPIView.as_view(), name="section_update"),
    path("section/destroy/", SectionDestroyAPIView.as_view(), name="section_destroy"),
    path("material/create/", MaterialCreateAPIView.as_view(), name="material_create"),
    path("material/list/", MaterialListAPIView.as_view(), name="material_list"),
    path("material/detail/", MaterialRetrieveAPIView.as_view(), name="material_detail"),
    path("material/update/", MaterialUpdateAPIView.as_view(), name="material_update"),
    path(
        "material/destroy/", MaterialDestroyAPIView.as_view(), name="material_destroy"
    ),
]
