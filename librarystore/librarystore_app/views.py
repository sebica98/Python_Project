from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Navbar, Book
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from cart.cart import Cart
from django.db.models import Sum


# Create your views here.
@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Book.objects.get(id=id)
    if product.stock == 0:
        return HttpResponse("Out of stock")
    cart.add(product=product)
    product.stock -= 1
    product.save()
    return redirect("books")


@login_required()
def item_clear(request, id):
    cart = Cart(request)
    product = Book.objects.get(id=id)
    cart.remove(product)
    return redirect("cart")


@login_required()
def item_increment(request, id):
    cart = Cart(request)
    product = Book.objects.get(id=id)
    if product.stock == 0:
        return HttpResponse("Out of stock")
    cart.add(product=product)
    product.stock -= 1
    product.save()
    return redirect("cart")


@login_required()
def item_decrement(request, id):
    cart = Cart(request)
    product = Book.objects.get(id=id)
    cart.decrement(product=product)
    product.stock += 1
    product.save()
    return redirect("cart")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    products = cart.restore_stock(request)
    for key, value in products.items():
        book = Book.objects.get(id=key)
        book.stock += value
        book.save()
    cart.clear()
    return redirect("cart")


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


def show_cart(request):
    navbar_items = Navbar.objects.all()
    cart = Cart(request)
    cart_sum = cart.get(request)
    return render(request, 'librarystore_app/cart_list.html', {'navbar_items': navbar_items,
                                                               'cart_sum': cart_sum})


def login_view(request):
    navbar_items = Navbar.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else: 
            return HttpResponse("Invalid Login")
    return render(request, 'librarystore_app/login.html', {'navbar_items':navbar_items})


def signup_view(request):
    navbar_items = Navbar.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'librarystore_app/register.html', {'form': form, 
                                                              'navbar_items':navbar_items})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/')