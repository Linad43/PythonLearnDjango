from catalog.models import Product, Category

category_phone = Category(name='Смартфоны', description='Многофункциональные электронные устройства')
category_food = Category(name='Еда', description='То что употребляется в пищу')
category_phone.save()
category_food.save()

products = [
    Product(name='Яблоко', price=10, category=category_food),
    Product(name='Груша', price=15, category=category_food),
    Product(name='Пицца', price=30, category=category_food),
    Product(name='Смартфон простой', price=5000, category=category_phone),
    Product(name='Крутой телефон', price=10000, category=category_phone)
]

for product in products:
    product.save()

categories = Category.objects.all()
for category in categories:
    print(category.name)
print('---')

products = Product.objects.all()
for product in products:
    print(product.name, product.price, product.category.name)
print('---')

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

products.delete()
categories.delete()
