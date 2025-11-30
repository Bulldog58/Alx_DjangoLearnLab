# advanced_features_and_security/relationship_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings 
# ... (other imports like post_save, receiver if you kept them)

# --- Custom User Manager and Model ---
class UserProfile(models.Model):
    # This must use the setting, which uses the correct capitalization
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    # ...

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        # ... logic to create standard user ...
        pass

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # ... logic to set superuser flags and call create_user ...
        pass

class CustomUser(AbstractUser):
    # ... fields ...
    objects = CustomUserManager() # <-- This assignment is critical


# --- Book Model (Missing piece) ---
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    # Add your custom permissions Meta class here from Task 4
    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book entry"),
            ("can_change_book", "Can edit an existing book entry"),
            ("can_delete_book", "Can delete a book entry"),
        ]

    def __str__(self):
        return self.title

# NOTE: If you had other models like UserProfile, they need to be here too,
# and ensure they use settings.AUTH_USER_MODEL for ForeignKeys/OneToOneFields.