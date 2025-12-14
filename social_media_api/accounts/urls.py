# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView, 
    UserLoginView, 
    UserProfileViewSet # Import the new ViewSet
)

# New router for the UserProfileViewSet
user_router = DefaultRouter()
user_router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = [
    # Existing routes
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    # New User Profile and Follow Routes
    path('', include(user_router.urls)), 
    
    # Simple profile route for current user (optional, can be replaced by /users/me/)
    # path('profile/', UserProfileView.as_view(), name='profile'), 
]

# Note on accessing follow endpoints:
# To follow user ID 5: POST /api/v1/auth/users/5/follow/
# To unfollow user ID 5: POST /api/v1/auth/users/5/unfollow/