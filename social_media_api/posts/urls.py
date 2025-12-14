from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikePostView, PostViewSet, CommentViewSet, PostFeedView, UnlikePostView


router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", PostFeedView.as_view(), name="post_feed"),


    # URLs for like and unlike actions
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='like_post'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='unlike_post'),
    path('notifications/', include('notifications.urls')),  # Add notifications URLs
]