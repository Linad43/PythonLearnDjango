# from typing import List
#
# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from .models import Product


class HomeView(TemplateView):
    template_name = "home.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"


class CatalogView(ListView):
    model = Product
    template_name = "catalog.html"
    context_object_name = "products"


class ProductDetailsView(DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"
    pk_url_kwarg = "id_product"
#
# def home(request):
#     return render(request, 'home.html')
#
#
# def contacts(request):
#     return render(request, 'contacts.html')
#
#
# def catalog(request):
#     return render(request,
#                   'catalog.html',
#                   {"products": Product.objects.all()}
#                   )
#
#
# def product_details(request, id_product):
#     product = Product.objects.get(id=id_product)
#     return render(request, 'product_details.html', {"product": product})
