from django.shortcuts import render
from .models import Product
from math import ceil
# Create your views here.

def index(request):
    prod = Product.objects.all()
    num_rows = ceil(len(prod)/4)
    return render(request, 'shop/index.html', {'products': prod, 'num_rows': range(num_rows) } )