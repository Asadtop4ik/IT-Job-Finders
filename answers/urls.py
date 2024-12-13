from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, get_answers_by_user, ContactViewSet, SmallWinViewSet
from django.urls import path

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register('answers', AnswerViewSet, basename='answers')
router.register('contact-us', ContactViewSet, basename='contacts')
router.register(r'smallwins', SmallWinViewSet)

urlpatterns = [
    path('answers/user/<int:user_id>/', get_answers_by_user, name='get_answers_by_user'),

] + router.urls

