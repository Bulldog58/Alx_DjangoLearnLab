# relationship_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    # ... (other Book fields) ...

    class Meta:
        # Define your custom permissions here
        permissions = [
            ("can_add_book", "Can add a new book entry"),
            ("can_change_book", "Can edit an existing book entry"),
            ("can_delete_book", "Can delete a book entry"),
        ]
        # Make sure to include the app_label if you are not in a model file
        # or if it's named differently, but generally not needed here.

    def __str__(self):
        return self.title
    
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