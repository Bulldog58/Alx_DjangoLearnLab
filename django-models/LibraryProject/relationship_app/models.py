# relationship_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define the user roles for clarity and reusability
class UserProfile(models.Model):
    # Role choices
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    # Link to the built-in User model (one-to-one relationship)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Role field with predefined choices, defaults to 'Member'
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f'{self.user.username} - {self.role}'


# Signal to automatically create UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Default the role to 'Member'
        UserProfile.objects.create(user=instance, role='Member')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure the UserProfile is saved when the User is saved
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Handle case where a User might exist without a profile (e.g., initial superuser)
        UserProfile.objects.create(user=instance, role='Member')