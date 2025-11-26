# relationship_app/views.py (Function-based view adjustment)

from django.shortcuts import render
# ... other imports ...

# --- Function-based View for Books ---
def book_list_view(request):
    """
    Function-based view to list all books.
    """
    # This line (Book.objects.all()) is required by the check
    books = Book.objects.all()
    
    context = {
        'books': books
    }
    
    # *** CRITICAL FIX: Change the template name here ***
    return render(request, 'relationship_app/list_books.html', context) 
    # Must use 'relationship_app/list_books.html'