import uuid

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse

import sys
from django.contrib.auth.models import User, Group

sys.path.append('D:\\3 SEM\\253503_TIMOSHEVICH_25\\IGI\\LR5\\LabRab5_IGI\\.venv\\Lib\\site-packages')


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=3)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Employees')
        self.user.groups.add(group)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        ordering = ["last_name", "first_name"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Shop Members')
        self.user.groups.add(group)


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturer-detail', args=[str(self.id)])


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.CASCADE, null=True)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True)

    # image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class ProductInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular product across whole shop")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customer = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (("can_mark_issued", "Set product as issued"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.product.name)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular product across whole shop")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInstance)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    LOAN_STATUS = (
        ('p', 'Processing'),
        ('s', 'Shipped'),
        ('d', 'Delivered'),
        ('i', 'Issued'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='p',
                              help_text='Status of the order')

    def save(self, *args, **kwargs):
        self.total_price = sum(product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.client}"


@receiver(m2m_changed, sender=Order.products.through)
def update_total_price(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        instance.total_price = sum(product_instance.product.price * product_instance.quantity for product_instance in instance.products.all())
        instance.save()