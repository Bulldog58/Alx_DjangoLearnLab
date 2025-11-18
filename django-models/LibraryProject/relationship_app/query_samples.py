import os
import django
import sys
import inspect

# --- CRITICAL FIX: Manually add the project root to the Python path ---
# This ensures the script can find 'LibraryProject' settings when run standalone.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
# ---------------------------------------------------------------------

# Set up Django environment manually for standalone script execution
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from django.db.models import Count

print("--- 1. Setting up Sample Data ---")

# --- Create Instances for All Models ---

# Create Author (The 'One' side of ForeignKey)
author_orwell, _ = Author.objects.get_or_create(name="George Orwell")
author_huxley, _ = Author.objects.get_or_create(name="Aldous Huxley")

# Create Books (The 'Many' side of ForeignKey)
book_1984, _ = Book.objects.get_or_create(title="1984", author=author_orwell)
book_brave, _ = Book.objects.get_or_create(title="Brave New World", author=author_huxley)
book_animal, _ = Book.objects.get_or_create(title="Animal Farm", author=author_orwell)

# Create Library (ManyToMany anchor)
library_central, _ = Library.objects.get_or_create(name="Central Branch")

# Add Books to Library (ManyToMany assignment)
# .add() is used for ManyToMany relationships
library_central.books.add(book_1984, book_brave, book_animal)

# Create Librarian (OneToOne anchor)
librarian_alice, _ = Librarian.objects.get_or_create(name="Alice Smith", library=library_central)

print("Setup Complete.\n")

# --------------------------------------------------------------------------------------------------

print("--- QUERY 1: Query all books by a specific author (ForeignKey/Reverse Lookup) ---")
# ForeignKey Reverse Lookup: Accesses 'Book' objects from the related 'Author' instance.
orwell_books = author_orwell.book_set.all()
print(f"Books by {author_orwell.name}:")
for book in orwell_books:
    print(f"  -> {book.title}")

print("\n--- QUERY 2: List all books in a library (ManyToManyField) ---")
# ManyToMany Lookup: Accesses the related 'Book' objects via the 'books' manager.
central_books = library_central.books.all()
print(f"Books in {library_central.name}:")
for book in central_books:
    print(f"  -> {book.title}")

print("\n--- QUERY 3: Retrieve the librarian for a library (OneToOne/Reverse Lookup) ---")
# OneToOne Reverse Lookup: Accesses the 'Librarian' object from the related 'Library' instance.
try:
    central_librarian = library_central.librarian
    print(f"Librarian for {library_central.name}: {central_librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian found for {library_central.name}")