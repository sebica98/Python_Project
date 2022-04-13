from django.shortcuts import render
from .models import Navbar, Book
from django.views.generic import ListView
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    navbar_items = Navbar.objects.all()
    book_items = Book.objects.filter(rating=5, is_bestselling=True)[:3]
    return render(request, 'librarystore_app/index.html', {'navbar_items': navbar_items,
                                                           'book_items': book_items})


class BookListView(ListView):
    model = Book
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_list'] = Navbar.objects.all()
        return context