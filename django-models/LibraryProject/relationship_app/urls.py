# relationship_app/urls.py (Verification)

from django.urls import path
from .views import book_list_view, LibraryDetailView # Ensure both are imported

urlpatterns = [
    # Function-based View (linked by name)
    path('books/', book_list_view, name='book-list'),
    
    # Class-based View (linked by .as_view())
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]