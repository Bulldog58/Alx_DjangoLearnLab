from django.urls import path
from .views import list_books, LibraryDetailView # Import both views

urlpatterns = [
    # URL pattern for the Function-Based View (FBV)
    path('books/', list_books, name='book-list'),
    
    # URL pattern for the Class-Based View (CBV)
    # Class-Based Views must be called with the .as_view() method
    path('books/<int:pk>/', LibraryDetailView.as_view(), name='book-detail'),
]