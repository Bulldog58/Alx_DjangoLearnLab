from django.urls import path
from .views import list_books, LibraryDetailView # Import both 
from django.urls import path
from .views import list_books, LibraryDetailView, register # Import the custom register view
from django.contrib.auth import views as auth_views # Import Django's built-in auth views


urlpatterns = [
    # Existing URL patterns
    path('books/', list_books, name='book-list'),
    path('books/<int:pk>/', LibraryDetailView.as_view(), name='book-detail'),
    
    # --- New Authentication URL Patterns ---
    
    # Registration View (Custom FBV)
    path('register/', register, name='register'),
    
    # Login View (Django's built-in View)
    # The 'template_name' points to relationship_app/templates/relationship_app/login.html
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Logout View (Django's built-in View)
    # The 'next_page' is where the user goes after logging out (e.g., back to login)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # URL pattern for the Function-Based View (FBV)
    path('books/', list_books, name='book-list'),
    
    # URL pattern for the Class-Based View (CBV)
    # Class-Based Views must be called with the .as_view() method
    path('books/<int:pk>/', LibraryDetailView.as_view(), name='book-detail'),
]