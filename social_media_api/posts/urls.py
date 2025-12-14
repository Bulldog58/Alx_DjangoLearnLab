# posts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
# Register the comment viewset for independent management (e.g., /comments/1/ for detail)
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Top-level routes for posts and independent comments (e.g., /api/v1/posts/)
    path('', include(router.urls)), 

    # Nested route for creating/listing comments under a post (e.g., /api/v1/posts/1/comments/)
    # Uses the custom 'comments' action defined in PostViewSet
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments-list'),
]