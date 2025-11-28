from django.urls import path
from .views import list_books, LibraryDetailView, register 
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

urlpatterns = [
    # Application Views
    path('books/', list_books, name='book-list'),
    path('books/<int:pk>/', LibraryDetailView.as_view(), name='book-detail'),
    
    # --- Authentication Views ---
    
    # Registration View (Custom FBV)
    # This correctly links to the 'register' function in .views
    path('register/', register, name='register'),
    
    # Login View (Built-in CBV)
    # Uses the LoginView class and points it to your login.html template
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Logout View (Built-in CBV)
    # Uses the LogoutView class and points it to your logout.html template
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'), 
    # NOTE: You can also use next_page='login' instead of template_name if you prefer
]