# posts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView # Import FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Feed endpoint
    path('feed/', FeedView.as_view(), name='user-feed'), # <-- New Feed route
    
    # Top-level routes for posts and independent comments
    path('', include(router.urls)), 

    # Nested route for comments
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments-list'),
]