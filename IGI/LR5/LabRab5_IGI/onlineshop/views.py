from django.shortcuts import render
from .models import Employee, Product, ProductType, Order, Client, Manufacturer


# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_products = Product.objects.all().count()
    num_manufacturers = Manufacturer.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_products': num_products, 'num_manufacturers': num_manufacturers},
    )


from django.views import generic


class ProductListView(generic.ListView):
    model = Product
    #paginate_by = 10  для постраничного отображения (надо обрабатывать в base_generic.html)


class ProductDetailView(generic.DetailView):
    model = Product
