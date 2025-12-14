# posts/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import generics

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    # Step 5: Filtering
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    # Step 5: Pagination will be applied globally or via custom settings

    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)
    
    # Custom action to list comments on a specific post
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        # Note: Pagination would ideally be applied here too
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        # Only return comments for the post specified in the URL (if used with nested routing)
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post_id=post_pk).order_by('created_at')
        return Comment.objects.all()

    def perform_create(self, serializer):
        # Automatically set the author and post
        post_pk = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        serializer.save(author=self.request.user, post=post)
 
class FeedView(generics.ListAPIView):
    """
    Returns a personalized feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Step 5: Pagination and Filtering are inherited from settings

    def get_queryset(self):
        # 1. Get the list of users the current user is following
        followed_users = self.request.user.following.all()
        
        # 2. Filter posts to include only those authored by the followed users
        #    and order them by creation date (most recent first)
        queryset = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        
        return queryset        