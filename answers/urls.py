from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, GeminiChatbotView
from django.urls import path

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register('answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('gemini-chat/', GeminiChatbotView.as_view(), name='gemini-chat'),

] + router.urls

