# relationship_app/views.py

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView # DetailView is required
# 👇 1. CRITICAL FIX: Ensure you import the Library model.
from .models import Book, Library # Must contain 'from .models import Library'

# --- (Other views like book_list_view remain the same) ---

# --- Class-based View for Library Detail (using DetailView) ---
class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library.
    """
    model = Library 
    
    # 👇 2. CRITICAL FIX: Ensure the template name is exactly this.
    template_name = 'relationship_app/library_detail.html'
    
    # 👇 3. CRITICAL FIX: Ensure the context object name is 'library'.
    context_object_name = 'library' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # This assumes the reverse relationship is named 'books'
        context['books'] = self.object.books.all() 
        return context