"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# relationship_app/urls.py
from django.urls import path
from .views import book_list_view, LibraryDetailView

urlpatterns = [
    # Route for the Function-based View (e.g., /app-name/books/)
    path('books/', book_list_view, name='book-list'),
    
    # Route for the Class-based View (e.g., /app-name/library/1/)
    # <int:pk> captures the primary key required by DetailView.
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]

