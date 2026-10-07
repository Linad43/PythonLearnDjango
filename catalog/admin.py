from django.contrib import admin

from mailings.models import Recipient, Message, Mailing, MailingAttempt
from .models import Category, Product


admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name','description')

