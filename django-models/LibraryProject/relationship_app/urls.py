from django.urls import path
from . import views

# Define the app namespace for use in templates and redirects (e.g., 'relationship_app:item_list')
app_name = 'relationship_app'

urlpatterns = [
    # 1. Route for the function-based view (e.g., listing all items)
    # The view 'item_list' must be defined as a function in views.py
    path('', views.item_list, name='item_list'),

    # 2. Route for the class-based DetailView
    # This path expects an integer primary key (pk) in the URL.
    # The view 'ItemDetailView' must be defined as a class in views.py
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
]