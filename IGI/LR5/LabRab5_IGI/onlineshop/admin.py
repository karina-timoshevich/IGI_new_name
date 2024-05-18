from django.contrib import admin
from .models import Employee, Product, ProductType, Order, Client, Manufacturer, UnitOfMeasure, ProductInstance


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
    list_display = ('name', 'price', 'product_type', 'manufacturer', 'unit_of_measure')
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
    list_display = ('user_username', 'first_name', 'last_name', 'user_email')
    search_fields = ('first_name', 'last_name', 'user_email')

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'  # Sets column header in admin panel

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username'  # Sets column header in admin panel


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'customer', 'id')
    # list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('product', 'id')
        }),
        ('Info', {
            'fields': ('quantity', 'customer')
        }),
    )
