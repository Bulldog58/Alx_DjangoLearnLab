# LibraryProject/views.py
from django.shortcuts import render
from django.views import View

def book_list_view(request):
    return render(request, 'some_template.html', {})

class LibraryDetailView(View):
    def get(self, request):
        return render(request, 'some_detail_template.html', {})