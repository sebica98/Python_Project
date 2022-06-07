import json
from turtle import title
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from kart.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from librarystore_app.models import Book
from librarystore_app.models import Navbar
from time import strftime
import datetime

# Create your views here.
def place_order(request):
    current_user = request.user
    
     # If the cart count <= 0, redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('books')
    
    grand_total = 0
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    if total >= 50:
        grand_total = total
    else:
        grand_total = total + 10

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") # 20220526
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            navbar_items = Navbar.objects.all().exclude(title='register')
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'grand_total': int(grand_total),
                'navbar_items': navbar_items
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('checkout')

def payment(request):

    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Check for the quantity of the sold product
    product = Book.objects.get(id=item.product_id)
    if product.stock < item.quantity:
        return HttpResponse('Out of stock')
    else:
        product.stock -= item.quantity
        product.save()

    payment = Payment(
        user = request.user,
        payment_id =  body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.is_ordered = True
    order.save()

    # Move the cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

    # Clear Cart
    CartItem.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

def order_complete(request):
    navbar_items = Navbar.objects.all().exclude(title='register')
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order_products = OrderProduct.objects.filter(order_id=order.id)
        context = {
            'order': order,
            'order_products': order_products,
            'navbar_items': navbar_items,
            'order_number': order.order_number,
            'transID': transID,
            'payment': payment,
        }
        return render(request, 'orders/order_complete.html', context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')