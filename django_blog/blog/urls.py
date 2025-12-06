from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, register, profile
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    # Blog Post URLs
    path('', PostListView.as_view(), name='home'),  
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'), 
    path('post/new/', PostCreateView.as_view(), name='post_create'),  
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'), 
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  

    # Comments URLs
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='create_comment'), 
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),  
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),  

    # Tags and Search URLs
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
    path('search/', views.search_view, name='search'),
]