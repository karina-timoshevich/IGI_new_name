import uuid

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse

import sys
from django.contrib.auth.models import User, Group

sys.path.append('D:\\3 SEM\\253503_TIMOSHEVICH_25\\IGI\\LR5\\LabRab5_IGI\\.venv\\Lib\\site-packages')

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=3)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='', null=True, blank=True)
    job_description = models.TextField(default='')  # new field
    phone = models.CharField(max_length=20, default='')  # new field
    email = models.EmailField(default='default@email.com')  # new field

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
    date_of_birth = models.DateField(null=True, blank=True)  # new field
    phone_number = models.CharField(max_length=20, default='', blank=True)  #

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

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        permissions = (("can_mark_issued", "Set product as issued"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.product.name)


class PickupLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular product across whole shop")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInstance)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)  # new field
    pickup_location = models.ForeignKey(PickupLocation, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Processing'),
        ('s', 'Shipped'),
        ('d', 'Delivered'),
        ('i', 'Issued'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='p',
                              help_text='Status of the order')

    def save(self, *args, **kwargs):
        self.total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        if self.promo_code:
            self.total_price *= (1 - self.promo_code.discount / 100)
        super().save(*args, **kwargs)

    def update_total_price(self):
        total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        if self.promo_code:
            total_price *= (1 - self.promo_code.discount / 100)
        self.total_price = total_price
        self.save()

    def __str__(self):
        return f"Order {self.id} by {self.client}"


@receiver(m2m_changed, sender=Order.products.through)
def update_total_price(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        instance.total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in instance.products.all())
        instance.save()


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInstance)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)  # new field

    def __str__(self):
        return f"Cart for {self.client}"

    def update_total_price(self):
        total_price = sum(
            product_instance.product.price * product_instance.quantity for product_instance in self.products.all())
        if self.promo_code:
            total_price *= (1 - self.promo_code.discount / 100)
        self.total_price = total_price
        self.save()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/')
    content = models.TextField()

    def __str__(self):
        return self.title


from django.db import models


class CompanyInfo(models.Model):
    text = models.TextField()
    video = models.FileField(upload_to='company_info/')
    logo = models.ImageField(upload_to='company_info/')
    history = models.TextField()
    details = models.TextField()

    def __str__(self):
        return "Company Information"
