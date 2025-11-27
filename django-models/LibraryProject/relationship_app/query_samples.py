# relationship_app/query_samples.py
import os
import django

# Replace 'your_project_name' with your actual main project name (e.g., LibraryProject)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings') 
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

# --- Query 1: Query all books by a specific author (ForeignKey) ---
def query_books_by_author(author_name: str) -> QuerySet:
    """Uses the reverse ForeignKey relationship (related_name='books')."""
    try:
        # Find the Author instance
        author = Author.objects.get(name=author_name)
        # Access all related books
        return Book.objects.filter(author=author)
    except ObjectDoesNotExist:
        return Book.objects.none()

# --- Query 2: List all books in a library (ManyToManyField) ---
def query_books_in_library(library_name: str) -> QuerySet:
    """Uses the forward ManyToMany relationship (Library.books.all())."""
    try:
        # Find the Library instance
        library = Library.objects.get(name=library_name)
        # Access all related books via the ManyToMany field
        return library.books.all() 
    except ObjectDoesNotExist:
        return Book.objects.none()

# 3. Retrieve the librarian for a library (OneToOne query)
def query_librarian_for_library(library_name: str) -> Librarian | None:
    """Retrieves the librarian using the Librarian model's OneToOne field lookup."""
    try:
        # Step 1: Find the Library instance (renamed to library_obj)
        library_obj = Library.objects.get(name=library_name)
        
        # Step 2: Query the Librarian model using the library instance
        # This explicitly uses the required lookup pattern: Librarian.objects.get(library=...)
        librarian = Librarian.objects.get(library=library_obj)
        
        # ... printing logic (optional) ...
        return librarian
    except ObjectDoesNotExist:
        # This handles cases where either the Library or the matching Librarian is not found.
        return None

if __name__ == '__main__':
    print("--- Sample Query Functions Defined ---")
    print("Run these functions in the Django shell after creating your models and sample data.")