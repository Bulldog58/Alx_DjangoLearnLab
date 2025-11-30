from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Ensure the Book model is present and looks like this (with custom permissions added)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(null=True, blank=True) # Added null/blank for flexibility

    class Meta:
        # Define the custom permissions here
        permissions = [
            ("can_view", "Can view book details"),
            ("can_create", "Can add a new book entry"),
            ("can_edit", "Can edit an existing book entry"),
            ("can_delete", "Can delete a book entry"),
        ]

    def __str__(self):
        return self.title
    
# Role choices for users
ROLE_CHOICES = (
    ("Admin", "Admin"),
    ("Librarian", "Librarian"),
    ("Member", "Member"),
)


class UserProfile(models.Model):
    """User profile model linked to CustomUser."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Automatically create a UserProfile when a new CustomUser is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile instance whenever a new user is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Ensure UserProfile updates when CustomUser is saved."""
    if hasattr(instance, 'userprofile'):  # Avoid errors if UserProfile doesn't exist
        instance.userprofile.save()


# Author model
class Author(models.Model):
    """Model for book authors."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Book model
class Book(models.Model):
    """Model for books in the library."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(default=timezone.now)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)

    class Meta:
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can edit a book"),
            ("can_delete_book", "Can delete a book"),
        ]

    def __str__(self):
        return self.title


# Library model
class Library(models.Model):
    """Model for a library containing books."""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


# Librarian model
class Librarian(models.Model):
    """Model for librarians managing a library."""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name