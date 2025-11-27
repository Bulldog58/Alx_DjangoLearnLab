# relationship_app/views.py
from django.shortcuts import render
from django.views.generic import DetailView
# Assuming these models exist from the previous task
from .models import Book, Library 

# --- 1. Function-based View (for listing books) ---
def book_list_view(request):
    """
    Lists all books using a function-based view and renders a template.
    """
    # Fetch all books
    books = Book.objects.all()
    
    context = {
        'books': books
    }
    
    # Renders the required template name for the book list check
    return render(request, 'relationship_app/list_books.html', context)

# --- 2. Class-based View (for library detail) ---
class LibraryDetailView(DetailView):
    """
    Displays a specific Library's details and its books using DetailView.
    """
    model = Library 
    # Sets the template name required for the library detail check
    template_name = 'relationship_app/library_detail.html' 
    # Sets the context name required for the library detail check
    context_object_name = 'library' 

    def get_context_data(self, **kwargs):
        # Calls the base implementation to get the Library object (self.object)
        context = super().get_context_data(**kwargs)
        
        # Add the list of related books (assuming reverse related_name='books' on Book model)
        context['books'] = self.object.books.all() 
        return context