# relationship_app/views.py

from django.shortcuts import render, redirect
from django.views import View # <-- Needed for the Class-Based View
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required # (Can be added later)


# 1. Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)


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