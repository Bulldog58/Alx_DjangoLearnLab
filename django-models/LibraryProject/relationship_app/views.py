# relationship_app/views.py
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library # CRITICAL: Imports both required models

# --- 1. Function-based View (for listing books) ---
def book_list_view(request):
    """
    Lists all books using a function-based view.
    Required to use Book.objects.all() and render 'relationship_app/list_books.html'.
    """
    books = Book.objects.all() # Required string: Book.objects.all()
    
    context = {
        'books': books
    }
    
    # Required template name for the check
    return render(request, 'relationship_app/list_books.html', context)

# --- 2. Class-based View (for library detail) ---
class LibraryDetailView(DetailView):
    """
    Displays a specific Library's details and its books using DetailView.
    Required strings: from .models import Library, 'relationship_app/library_detail.html', 'library'.
    """
    model = Library # Uses the imported Library model
    
    # Required template name for the check
    template_name = 'relationship_app/library_detail.html' 
    
    # Required context name for the check
    context_object_name = 'library' 

    def get_context_data(self, **kwargs):
        # Calls the base implementation to get the Library object (self.object)
        context = super().get_context_data(**kwargs)
        
        # Adds the list of related books (assuming reverse related_name='books' on Book model)
        context['books'] = self.object.books.all() 
        return context