from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ProductForm
from .models import Product
from .services import get_products_by_category


class HomeView(TemplateView):
    template_name = "home.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"


class CatalogView(ListView):
    model = Product
    template_name = "catalog.html"
    context_object_name = "products"


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailsView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"
    pk_url_kwarg = "id_product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Product
    template_name = "product_form.html"
    form_class = ProductForm
    pk_url_kwarg = "id_product"
    success_url = reverse_lazy("catalog:catalog")

    def test_func(self):
        return self.get_object().owner == self.request.user


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Product
    template_name = "product_confirm_delete.html"
    pk_url_kwarg = "id_product"
    success_url = reverse_lazy("catalog:catalog")

    def test_func(self):
        product = self.get_object()
        is_owner = product.user == self.request.user
        is_moderator = self.request.user.has_perm(
            'catalog.delete_product',
        )
        return is_owner or is_moderator


class ProductUnpublishView(
    LoginRequiredMixin,
    View,
):
    def post(self, request, id_product):
        product = get_object_or_404(Product, pk=id_product)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        product.published = False
        product.save(update_fields=['published'])
        return redirect(
            'catalog:product_details',
            id_product=product.pk,
        )


class ProductsByCategoryView(TemplateView):
    template_name = "products_by_category.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        context["products"] = get_products_by_category(category_id)
        return context
