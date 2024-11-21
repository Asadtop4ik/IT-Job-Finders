from django.urls import path
from .views import GPTView

urlpatterns = [
    path('gpt/', GPTView.as_view(), name='gpt-api'),
]
