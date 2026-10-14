from django.urls import path

from .views import (
    HSKLevelListView,
    QuizAnswerView,
    QuizBatchAnswerView,
    QuizQuestionListView,
    QuizQuestionView,
    StudyWordListView,
)

urlpatterns = [
    path("levels/", HSKLevelListView.as_view(), name="hsk-levels"),
    path("study/", StudyWordListView.as_view(), name="study-words"),
    path("quiz/question/", QuizQuestionView.as_view(), name="quiz-question"),
    path("quiz/questions/", QuizQuestionListView.as_view(), name="quiz-questions"),
    path("quiz/answer/", QuizAnswerView.as_view(), name="quiz-answer"),
    path("quiz/answers/", QuizBatchAnswerView.as_view(), name="quiz-batch-answers"),
]