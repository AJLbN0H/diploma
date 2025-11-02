from django.urls import path, include
from rest_framework.routers import SimpleRouter

from tests.views import (
    TestViewSet,
    QuestionViewSet,
    AnswerViewSet,
    TestResultDestroyAPIView,
    TestResultListAPIView, TestDetailAPIView, TestSubmitView, TestResultRetrieveAPIView,
)

app_name = "tests"

router = SimpleRouter()
router.register("test", TestViewSet, basename="test")
router.register("question", QuestionViewSet, basename="question")
router.register("answer", AnswerViewSet, basename="answer")

urlpatterns = [
    path("", include(router.urls)),
    path('detail/<int:pk>/', TestDetailAPIView.as_view(), name='test_detail'),
    path('submit/<int:test_id>/', TestSubmitView.as_view(), name='test_submit'),
    path('results/', TestResultListAPIView.as_view(), name='test_results'),
    path('results/<int:pk>/detail/', TestResultRetrieveAPIView.as_view(), name='test_result_detail'),
    path('results/<int:pk>/delete/', TestResultDestroyAPIView.as_view(), name='test_result_destroy'),
]
