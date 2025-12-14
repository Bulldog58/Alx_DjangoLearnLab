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