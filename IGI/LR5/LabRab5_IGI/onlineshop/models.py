from django.db import models
from django.urls import reverse
# import "D:\3 SEM\253503_TIMOSHEVICH_25\IGI\LR5\LabRab5_IGI\.venv\Lib\site-packages\PIL"
# from PIL import Image
# import image
import sys

sys.path.append('D:\\3 SEM\\253503_TIMOSHEVICH_25\\IGI\\LR5\\LabRab5_IGI\\.venv\\Lib\\site-packages')


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    # employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name"]


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.client}"
