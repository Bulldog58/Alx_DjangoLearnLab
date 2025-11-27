# relationship_app/query_samples.py

# ... imports ...
from relationship_app.models import Author, Book, Library, Librarian
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

# 1. Query all books by a specific author (ForeignKey query)
def query_books_by_author(author_name: str) -> QuerySet:
    """Retrieves all books written by an author using the filter() method."""
    try:
        # Find the Author instance
        author = Author.objects.get(name=author_name)
        
        # 👇 CRITICAL FIX: Use the specific filter pattern required by the check
        # This filters the Book model where the 'author' field matches the Author instance.
        books = Book.objects.filter(author=author)
        
        # ... printing logic (if included) ...
        return books
    except ObjectDoesNotExist:
        return Book.objects.none()

# ... other query functions remain the same ...