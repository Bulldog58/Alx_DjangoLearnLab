# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer
from .models import User

# --- 1. Registration View (POST /register) ---
class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate and return token immediately upon registration
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- 2. Login View (POST /login) ---
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Retrieve or create token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- 3. Profile Management View (GET/PUT /profile) ---
class UserProfileView(generics.RetrieveUpdateAPIView):
    # Only authenticated users can access their profile
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # The object is the currently authenticated user
        return self.request.user