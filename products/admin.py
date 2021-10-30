from django.contrib import admin

from .models import Product
# Register your models here.

# making a column for displaying the name of slug in admin's page product list
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Product
# also second step for line 6 operation is adding ProductAdmin
admin.site.register(Product, ProductAdmin)

