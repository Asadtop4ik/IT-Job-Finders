from django.urls import path
from .views import GPTAPIView

urlpatterns = [
    path('gpt/', GPTAPIView.as_view(), name='gpt-api'),
]
