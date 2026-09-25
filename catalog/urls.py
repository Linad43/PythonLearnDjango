from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    HomeView,
    ContactsView,
    CatalogView,
    ProductDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductUnpublishView
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("product_details/<int:id_product>/", ProductDetailsView.as_view(), name="product_details"),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
    path("product_update/<int:id_product>/", ProductUpdateView.as_view(), name="product_update"),
    path("product_delete/<int:id_product>/", ProductDeleteView.as_view(), name="product_delete"),
path("product_unpublish/<int:id_product>/", ProductUnpublishView.as_view(), name="product_unpublish"),
]
