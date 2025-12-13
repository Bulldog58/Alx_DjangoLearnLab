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