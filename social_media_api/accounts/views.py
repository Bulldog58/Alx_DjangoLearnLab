from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer
)
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# 1. Registration View (POST /api/v1/auth/register)
class UserRegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        # We override post to return a custom response after successful registration
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "User registered successfully."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


# 2. Login View (POST /api/v1/auth/login)
# This view is based on the logic in UserLoginSerializer
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Token is generated/retrieved inside the serializer's validate method
        token = serializer.validated_data['token']
        
        return Response({
            'token': token,
            'user_id': serializer.validated_data['user'].pk,
            'email': serializer.validated_data['user'].email
        })


# 3. Profile View (GET/PUT /api/v1/auth/profile)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,) # Requires a valid token

    # The user can only view/edit their own profile
    def get_object(self):
        return self.request.user

class UserProfileViewSet(viewsets.ModelViewSet):
    # This viewset is for managing the user profile, including follow actions.
    queryset = UserModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override list/retrieve to ensure fields are correct
    def get_object(self):
        # Allow users to retrieve their own profile or any other user's profile
        if self.action in ['retrieve', 'update', 'partial_update']:
            # For detail actions, we use the primary key from the URL or the current user
            lookup_field = self.kwargs.get('pk')
            if lookup_field:
                return self.get_queryset().get(pk=lookup_field)
            return self.request.user
        return self.request.user # Default to the current user

    # Custom action to follow a user (POST /api/v1/auth/users/{pk}/follow/)
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        target_user = self.get_object()
        current_user = request.user

        if current_user == target_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add target_user to the current user's 'following' set
        # The 'following' set is managed via the 'followers' M2M field
        current_user.following.add(target_user)
        
        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)

    # Custom action to unfollow a user (POST /api/v1/auth/users/{pk}/unfollow/)
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        target_user = self.get_object()
        current_user = request.user

        if current_user == target_user:
            return Response({"detail": "Invalid operation."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove target_user from the current user's 'following' set
        current_user.following.remove(target_user)
        
        return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)