from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, get_answers_by_user
from django.urls import path

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register('answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('answers/user/<int:user_id>/', get_answers_by_user, name='get_answers_by_user'),

] + router.urls

