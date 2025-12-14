from .models import Post, Comment, Like
from notifications.utils import create_notification
from rest_framework import viewsets, permissions, filters, status 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        # Use generics.get_object_or_404 for retrieving the post
        post = generics.get_object_or_404(Post, pk=pk)

        # Use get_or_create to ensure a like is created only if it doesn't exist
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "You have already liked this post."}, status=400)

        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id,
        )

        return Response({"detail": "Post liked successfully"}, status=200)

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        # Use generics.get_object_or_404 for retrieving the post
        post = generics.get_object_or_404(Post, pk=pk)

        # Check if the user has liked the post
        like = Like.objects.filter(post=post, user=request.user).first()
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=400)

        # Delete the like
        like.delete()

        # Optionally, delete the notification
        Notification.objects.filter(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id,
        ).delete()

        return Response({"detail": "Post unliked successfully"}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the current user
        user = request.user

        # Get the list of users that the current user is following
        following_users = user.following.all()

        # Fetch posts from the followed users, ordered by creation date (most recent first)
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Use generics.get_object_or_404 for retrieving the post
        post = generics.get_object_or_404(Post, pk=pk)

        user = request.user

        # Prevent users from liking their own posts
        if post.author == user:
            return Response(
                {"detail": "You cannot like your own post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure a like is created only if it doesn't exist
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author, actor=user, verb="liked your post", target=post
        )

        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED
        )


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Use generics.get_object_or_404 for retrieving the post
        post = generics.get_object_or_404(Post, pk=pk)

        user = request.user

        # Ensure the user has liked the post
        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response(
                {"detail": "You haven't liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Delete the like
        like.delete()

        return Response(
            {"detail": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT
        )