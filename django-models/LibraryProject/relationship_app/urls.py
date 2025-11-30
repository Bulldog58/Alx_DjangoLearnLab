# relationship_app/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    list_books, LibraryDetailView, register, admin_view, librarian_view,
    member_view, add_book, edit_book, delete_book
)

urlpatterns = [
    # ... (Existing paths: books/, register/, login/, logout/) ...

# --- Secured Book CRUD URLs ---
    path('books/add/', add_book, name='book-add'),
    path('books/<int:pk>/edit/', edit_book, name='book-edit'),
    path('books/<int:pk>/delete/', delete_book, name='book-delete'),

    # --- Role-Based Access URLs ---
    path('admin-dashboard/', admin_view, name='admin-dashboard'),
    path('librarian-panel/', librarian_view, name='librarian-panel'),
    path('member-area/', member_view, name='member-area'),
    
    # URL for the 'Member' view
    path('member-area/', member_view, name='member-area'), # <-- Links to the function

    # Application Views
    path('books/', list_books, name='book-list'),
    path('books/<int:pk>/', LibraryDetailView.as_view(), name='book-detail'),
    
    # --- Authentication Views ---
    
    # Registration View (Fix: links to views.register)
    path('register/', register, name='register'),
    
    # Login View (Built-in CBV)
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Logout View (Built-in CBV)
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
]