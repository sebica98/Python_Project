from ast import Pass
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Navbar, Book, Author
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from cart.cart import Cart
from rest_framework import viewsets, generics
from .serializers import BookSerializer, AuthorSerializer, UserSerializer
from .forms import UpdateUserForm, PasswordChangeForm


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
    if request.user.is_authenticated:
        navbar_items = Navbar.objects.all().exclude(title="Register")
    else:
        navbar_items = Navbar.objects.all()
    book_items = Book.objects.filter(rating=5, is_bestselling=True)[:3]
    return render(request, 'librarystore_app/index.html', {'navbar_items': navbar_items,
                                                           'book_items': book_items})


class BookListView(ListView):
    model = Book
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_items'] = Navbar.objects.all()
        return context

@login_required(login_url='/login/')
def show_cart(request):
    navbar_items = Navbar.objects.all().exclude(title="Register")
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


@login_required(login_url='/login/')
def purchase_view(request):
    navbar_items = Navbar.objects.all().exclude(title="Register")
    cart = Cart(request)
    cart_sum = cart.get(request)
    return render(request, 'librarystore_app/checkout.html', {'navbar_items': navbar_items,
                                                              'cart_sum': cart_sum})

@login_required(login_url='/login/')
def user_profile(request):
    navbar_items = Navbar.objects.all().exclude(title="Register")
    cart = Cart(request)
    cart_sum = cart.get(request)
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST,instance=request.user)
        p_form = PasswordChangeForm(data=request.POST, user=request.user)
        if u_form.is_valid() or p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your password and name were changed!')
            return redirect('/')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = PasswordChangeForm(user=request.user)
    return render(request, 'librarystore_app/user_profile.html', {'navbar_items': navbar_items,
                                                                  'u_form': u_form,
                                                                  'p_form': p_form,
                                                                  'cart_sum': cart_sum,
                                                                  })

class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
