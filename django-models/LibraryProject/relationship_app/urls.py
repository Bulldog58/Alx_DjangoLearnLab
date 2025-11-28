from django.urls import path
from .views import list_books, LibraryDetailView, register # <-- Make sure 'register' is imported
from django.contrib.auth import views as auth_views 

urlpatterns = [
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