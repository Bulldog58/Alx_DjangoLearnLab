from django.db import models

class Book(models.Model):
    """
    Model representing a book in the library with title, author, and publication year.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        # Human-readable representation for the Django shell and Admin
        return f"{self.title} ({self.publication_year})"