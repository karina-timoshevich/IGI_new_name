from django.contrib import admin
from .models import Employee, Product, ProductType, Order, Client, Manufacturer


# Register your models here.
# admin.site.register(Employee)
# admin.site.register(Product)
# admin.site.register(ProductType)
# admin.site.register(Order)
# admin.site.register(Client)
# admin.site.register(Manufacturer)

# Define the admin class
class EmpoyeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position')
    pass


# Register the admin class with the associated model
admin.site.register(Employee, EmpoyeeAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'product_type', 'manufacturer')
    list_filter = ('name', 'price')
    pass

class ProductsInstanceInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductsInstanceInline]


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'order_date')
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    pass
