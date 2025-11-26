# relationship_app/views.py
from django.views.generic import DetailView
from django.shortcuts import render 
# ... other imports ...

# 👇 CRITICAL FIX 1: Must contain 'from .models import Library'
from .models import Book, Library 

# --- Class-based View for Library Detail ---
class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library.
    """
    model = Library 
    
    # 👇 CRITICAL FIX 2: Must contain 'relationship_app/library_detail.html'
    template_name = 'relationship_app/library_detail.html'
    
    # 👇 CRITICAL FIX 3: Must contain 'library' (as context_object_name)
    context_object_name = 'library' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assumes the reverse relationship name on Library is 'books'
        context['books'] = self.object.books.all() 
        return context