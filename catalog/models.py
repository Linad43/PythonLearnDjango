from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {str(self.price)}"

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']
