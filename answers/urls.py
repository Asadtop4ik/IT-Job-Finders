from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet
from django.urls import path
router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')  # Endpoint for questions
router.register('answers', AnswerViewSet, basename='answers')


urlpatterns = [


] + router.urls



