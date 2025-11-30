# relationship_app/views.py

from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login # <-- Add this import
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    # Check if the user is authenticated and has the 'Admin' role
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    # Check if the user is authenticated and has the 'Librarian' role
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    # Check if the user is authenticated and has the 'Member' role
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# --- Role-Based Views ---

@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    # Access granted only if is_admin(request.user) is True
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    # Access granted only if is_librarian(request.user) is True
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(is_member, login_url='login')
def member_view(request):
    # Access granted only if is_member(request.user) is True
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})

# --- Helper Functions for Role Checking ---

# 1. Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # <-- Save the user object to a variable
            login(request, user) # <-- Log the user in immediately
            # Redirect them to the homepage or book list after successful login/registration
            return redirect('book-list') # Assuming 'book-list' is a valid name
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)


# ... (list_books and LibraryDetailView remain the same)


# 2. Function-Based View (list_books)
def list_books(request):
    # This is required because relationship_app/urls.py tries to import it.
    # Replace the placeholder with your actual logic later.
    return render(request, 'relationship_app/book_list.html', {'message': 'Book List View'})


# 3. Class-Based View (LibraryDetailView)
class LibraryDetailView(View):
    # This is required because relationship_app/urls.py tries to import it.
    # Replace the placeholder with your actual logic later.
    def get(self, request, pk):
        return render(request, 'relationship_app/book_detail.html', {'pk': pk, 'message': 'Book Detail View'})