from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProfileUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # User registration
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # Token-based login
    path('profile/', ProfileUserView.as_view(), name='profile'),  # Retrieve logged-in user profile
]
