# relationship_app/urls.py

# Ensure 'member_view' is in the imports at the top
from .views import ..., member_view
from django.urls import path
from .views import list_books, LibraryDetailView, register, admin_view, librarian_view, member_view # <-- FIX: Add the three views here
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... (Existing paths: books/, register/, login/, logout/) ...

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