# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import UserProfileSerializer # Reuse the profile serializer for author details

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at')
        read_only_fields = ('author', 'post', 'created_at', 'updated_at')
        extra_kwargs = {
            'post': {'write_only': True} # Post ID is passed in URL, not body
        }

class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True) # Display full author details
    comments = CommentSerializer(many=True, read_only=True) # Nested comments (optional, for detail view)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count')
        read_only_fields = ('author', 'created_at', 'updated_at', 'comments', 'comment_count')

    def get_comment_count(self):
        # Calculate the number of comments for the post
        return self.instance.comments.count() if self.instance else 0