from django.urls import path
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

app_name = 'tests'

router = SimpleRouter()
router.register("test/", TestViewSet)
router.register("question/", QuestionViewSet)
router.register("answer/", AnswerViewSet)

urlpatterns = [
    path(
        "test/result/create/",
        TestResultCreateAPIView.as_view(),
        name="test_result_create",
    ),
    path("test/result/list/", TestResultListAPIView.as_view(), name="test_result_list"),
    path(
        "test/result/retrieve/",
        TestResultRetrieveAPIView.as_view(),
        name="test_result_retrieve",
    ),
    path(
        "test/result/delete/",
        TestResultDestroyAPIView.as_view(),
        name="test_result_delete",
    ),
] + router.urls
