from django.urls import path

from tests.views import TestViewSet, QuestionViewSet, AnswerViewSet, TestResultCreateAPIView, TestResultDestroyAPIView, \
    TestResultListAPIView, TestResultRetrieveAPIView

urlpatterns = [
    path("test/", TestViewSet.as_view(), name="test"),
    path("question/", QuestionViewSet.as_view(), name="question"),
    path("answer/", AnswerViewSet.as_view(), name="answer"),
    path("test/result/create/", TestResultCreateAPIView.as_view(), name="test_result_create"),
    path("test/result/list/", TestResultListAPIView.as_view(), name="test_result_list"),
    path("test/result/retrieve/", TestResultRetrieveAPIView.as_view(), name="test_result_retrieve"),
    path("test/result/delete/", TestResultDestroyAPIView.as_view(), name="test_result_delete"),
]
