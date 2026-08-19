from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Test catalog DB'

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        for category in categories:
            print(category.name)
        print('---')

        products = Product.objects.all()
        for product in products:
            print(product.name, product.price, product.category.name)
        print('---')

        category_food = Category.objects.get(name='Еда')
        products_food = Product.objects.filter(category=category_food)
        for product in products_food:
            print(product.name, product.price, product.category.name)
        print('---')

        apple = Product.objects.get(name="Яблоко")
        apple.price = 8
        apple.save()
        print(apple)

        pear = Product.objects.get(name="Груша")
        pear.delete()
