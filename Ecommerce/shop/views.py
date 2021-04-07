from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, Cart
from math import ceil
from django.contrib import messages
from django.utils import timezone
from user.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    all_products = []
    prod = Product.objects.all()
    catProds = Product.objects.values('product_category')
    cats = {item['product_category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        all_products.append(prod)
    return render(request, 'shop/index.html', {'all_products': all_products})


def detail_product(request, id):
    product = Product.objects.filter(id=id)
    return render(request, 'shop/productDetailed.html', {'product': product[0]})

@login_required
def cart(request):
    cart = Cart.objects.filter(user = request.user, cart_status=False)
    total_price = 0
    for item in cart:
        total_price += int(item.total_price())
    context = {'cart':cart, 'total_price': total_price}
    return render(request, 'shop/cart.html', context)

@login_required
def checkout(request):
    user = User.objects.filter(username = request.user.username)[0]
    cart = Cart.objects.filter(user = request.user, cart_status=False)
    total_price = 0
    total_items = 0
    for item in cart:
        total_price += int(item.total_price())
        total_items += item.quantity
    order = Order.objects.filter(user=request.user, order_status=False)[0]
    order.order_price = total_price
    order.order_items = total_items
    order.save()
    context = {'cart':cart, 'total_price': total_price, 'user':user}
    return render(request, 'shop/checkout.html', context)

@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(
        product=product, user=request.user, cart_status=False, cart_date = timezone.now())
    if created == True:
        cart.cart_date = timezone.now()
    order_state = Order.objects.filter(user=request.user, order_status=False)
    if order_state.exists():
        order = order_state[0]
        if order.products.filter(product=product).exists():
            cart.quantity += 1
            messages.info(request, "Product quantity updated")
        else:
            order.products.add(cart)
            cart.quantity = 1
            messages.info(request, "Product Added to the cart")
    else:
        order = Order.objects.create(
            user=request.user)
        order.products.clear()
        order.products.add(cart)
        cart.quantity = 1
        messages.info(request, "Product Added to the cart")
    cart.save()
    return redirect('detail-product', id=id)

@login_required
def remove_from_cart(request, id):
    product = Product.objects.get(id=id)
    order_state = Order.objects.filter(user=request.user, order_status=False)
    if order_state.exists():
        order = order_state[0]
        if order.products.filter(product=product).exists():
            cart = Cart.objects.filter(
                product=product, user=request.user, cart_status=False)[0]
            if cart.quantity == 1:
                cart.quantity = 0
                order.products.remove(cart)
                cart.save()
                messages.info(request, "Product removed from the cart")
            else:
                cart.quantity -= 1
                cart.save()
                messages.info(request, "Product quantity updated")
        else:
            messages.warning(
                request, "The product does not exist in your cart")
    else:
        messages.warning(request, "No items in the cart")
    return redirect('detail-product', id=id)

@login_required
def order_confirm(request):
    Cart.objects.filter(user = request.user, cart_status=False).update(cart_status = True)
    order = Order.objects.filter(user=request.user, order_status=False)[0]
    order.order_status = True
    order.order_date = timezone.now()
    order.order_address = request.user.profile.address
    order.save()
    return render(request, 'shop/orderConfirm.html')