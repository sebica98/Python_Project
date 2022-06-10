from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from orders.models import Order
from librarystore_app.models import Navbar
from .forms import UserForm

# Create your views here.
@login_required(login_url = 'login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    navbar_items = Navbar.objects.all().exclude(title='register')
    context = {
        'navbar_items': navbar_items,
    }
    return render(request, 'accounts/change_password.html', context)

@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    navbar_items = Navbar.objects.all().exclude(title='register')

    context = {
        'orders_count': orders_count,
        'navbar_items': navbar_items,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    navbar_items = Navbar.objects.all().exclude(title='register')
    context = {
        'orders': orders,
        'navbar_items': navbar_items,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url = 'login')
def edit_profile(request):
    navbar_items = Navbar.objects.all().exclude(title='register')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)

    context = {
        'navbar_items': navbar_items,
        'user_form': user_form,
    }
    return render(request, 'accounts/edit_profile.html', context)