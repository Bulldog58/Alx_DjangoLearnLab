# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(
        max_length=500, 
        blank=True,
        help_text="A short biography about the user."
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True,
        help_text="Path to the user's profile image."
    )
    # Self-referential ManyToMany field for followers/following
    # symmetrical=False: Allows a user to follow another without mutual following
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following', 
        blank=True,
        help_text="Users who follow this user."
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class CustomUser(AbstractUser):
    # Additional fields defined previously
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Many-to-Many field for followers (already fine)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    # 🛑 FIX 1: Add custom related_name for the 'groups' field
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set", # 👈 THE FIX
        related_query_name="custom_user",
    )

    # 🛑 FIX 2: Add custom related_name for the 'user_permissions' field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="custom_user_permissions_set", # 👈 THE FIX
        related_query_name="custom_user",
    )
    
    def __str__(self):
        return self.username