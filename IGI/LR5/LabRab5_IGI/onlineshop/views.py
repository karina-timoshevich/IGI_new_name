from django.shortcuts import render
from .models import Employee, Product, ProductType, Order, Client, Manufacturer, UnitOfMeasure, ProductInstance


# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_products = Product.objects.all().count()
    num_manufacturers = Manufacturer.objects.count()  # Метод 'all()' применён по умолчанию.
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_products, 'num_authors': num_manufacturers,
                 'num_visits': num_visits},  # num_visits appended
    )


from django.views import generic


class ProductListView(generic.ListView):
    model = Product
    # paginate_by = 10  для постраничного отображения (надо обрабатывать в base_generic.html)


class ProductDetailView(generic.DetailView):
    model = Product


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    pass


class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer
    pass


from django.contrib.auth.mixins import LoginRequiredMixin


class OrderedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = ProductInstance
    template_name = 'onlineshop/productinstance_list_ordered_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(customer=self.request.user)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import ProductInstance

class AllOrdersForEmployeeView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all orders, accessible only to employees.
    """
    model = ProductInstance
    template_name = 'onlineshop/productinstance_list_all_orders.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ProductInstance.objects.all()