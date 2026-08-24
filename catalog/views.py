from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, 'home.html')


def contacts(request):
    return render(request, 'contacts.html')


def catalog(request):
    return render(request, 'catalog.html', {"products": Product.objects.all()})

def product_details(request, id_product):
    product = Product.objects.get(id=id_product)
    return render(request, 'product_details.html', {"product": product})