# accounts/serializers.py

from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

# --- 1. Registration Serializer ---
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        # Include fields required for registration
        fields = ('id', 'username', 'email', 'password', 'bio')
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        # Use create_user to ensure password hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        return user

# --- 2. Login Serializer ---
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                    return data
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Incorrect credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

# --- 3. User Profile Serializer (for GET /profile) ---
class UserProfileSerializer(serializers.ModelSerializer):
    # Count followers/following dynamically
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture', 
            'date_joined', 'followers_count', 'following_count'
        ]
        read_only_fields = ['username', 'email', 'date_joined']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    