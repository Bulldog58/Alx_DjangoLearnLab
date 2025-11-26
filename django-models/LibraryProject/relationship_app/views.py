# relationship_app/views.py

from django.shortcuts import render
# Ensure Book is imported if you haven't already
from .models import Book, Library 
# ... other imports ...

# --- Function-based View for Books ---
def book_list_view(request):
    """
    Function-based view to list all books.
    """
    # 1. CRITICAL: This line must be present.
    books = Book.objects.all()
    
    context = {
        'books': books
    }
    
    # 2. CRITICAL: The template name must be exactly 'relationship_app/list_books.html'.
    return render(request, 'relationship_app/list_books.html', context)