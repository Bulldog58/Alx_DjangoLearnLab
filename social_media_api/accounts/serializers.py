from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

UserModel = get_user_model()

# 1. Registration Serializer (Creates a new user)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'password2', 'bio')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'bio': {'required': False},
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        # Securely create the user using the create_user method
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        return user


# 2. Login Serializer (Authenticates user and retrieves token)
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            # Authenticate credentials
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        # Get or create the token for the user
        token, created = Token.objects.get_or_create(user=user)

        data['token'] = token.key
        data['user'] = user # Attach user object to validated data
        return data


# 3. Profile Serializer (Used for fetching or updating profile data)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following')
        read_only_fields = ('username', 'email', 'followers', 'following') # Only bio/pic is editable