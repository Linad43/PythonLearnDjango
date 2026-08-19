from os import name

from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add test catalog to the database'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        categories = [
            {'name': 'Смартфон', 'description': 'Многофункциональные электронные устройства'},
            {'name': 'Еда', 'description': 'То что употребляется в пищу'},
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(**category_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        products = [
            {'name': 'Яблоко', 'price': '10', 'category': Category.objects.get(name='Еда')},
            {'name': 'Груша', 'price': '15', 'category': Category.objects.get(name='Еда')},
            {'name': 'Пицца', 'price': '30', 'category': Category.objects.get(name='Еда')},
            {'name': 'Смартфон простой', 'price': '5000', 'category': Category.objects.get(name='Смартфон')},
            {'name': 'Крутой телефон', 'price': '10000', 'category': Category.objects.get(name='Смартфон')},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added product: {product.name} {product.price}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Student already exists: {product.name} {product.price}'))
