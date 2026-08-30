from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeView, ContactsView, CatalogView, ProductDetailsView

# from catalog.views import home, contacts, catalog, product_details

app_name = CatalogConfig.name

# urlpatterns = [
#     path("", home, name="home"),
#     path("contacts/", contacts, name="contacts"),
#     path("catalog/", catalog, name="catalog"),
#     path("product_details/<int:id_product>/", product_details, name="product_details"),
# ]

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("product_details/<int:id_product>/", ProductDetailsView.as_view(), name="product_details"),
]
