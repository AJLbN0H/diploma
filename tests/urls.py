from django.urls import path, include
from rest_framework.routers import SimpleRouter

from tests.views import (
    TestViewSet,
    QuestionViewSet,
    AnswerViewSet,
    TestResultCreateAPIView,
    TestResultDestroyAPIView,
    TestResultListAPIView,
    TestResultRetrieveAPIView,
)

app_name = "tests"

router = SimpleRouter()
router.register("test", TestViewSet, basename='test')
router.register("question", QuestionViewSet, basename='question')
router.register("answer", AnswerViewSet, basename='answer')

urlpatterns = [
    path(
        "test/result/create/",
        TestResultCreateAPIView.as_view(),
        name="test_result_create",
    ),
    path("test/result/", TestResultListAPIView.as_view(), name="test_result_list"),
    path(
        "test/result/retrieve/<int:pk>/",
        TestResultRetrieveAPIView.as_view(),
        name="test_result_retrieve",
    ),
    path(
        "test/result/delete/<int:pk>/",
        TestResultDestroyAPIView.as_view(),
        name="test_result_delete",
    ),
    path('', include(router.urls))
]
