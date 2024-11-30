from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='questions')  # Endpoint for questions
router.register('answers', AnswerViewSet, basename='answers')  # Endpoint for answers

urlpatterns = router.urls
