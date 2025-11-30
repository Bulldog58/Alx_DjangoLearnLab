from django import forms
from .models import Book  

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date']

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    author = forms.CharField(max_length=100, required=True)
    published_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    isbn = forms.CharField(max_length=13, required=True)