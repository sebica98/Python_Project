from django.shortcuts import render
from .models import Navbar, Book

# Create your views here.
def index(request):
    navbar_items = Navbar.objects.all()
    book_items = Book.objects.filter(rating=5, is_bestselling=True)
    return render(request, 'librarystore_app/index.html', {'navbar_items': navbar_items,
                                                           'book_items': book_items})