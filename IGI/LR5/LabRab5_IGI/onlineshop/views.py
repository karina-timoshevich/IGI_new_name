from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import FormView

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

from django.shortcuts import get_object_or_404


class OrderedProductsByUserListView(LoginRequiredMixin, generic.ListView):
    model = ProductInstance
    template_name = 'onlineshop/order_detail.html'
    paginate_by = 10

    def get_queryset(self):
        self.order = get_object_or_404(Order, id=self.kwargs.get('order_id'), client__user=self.request.user)
        return self.order.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'onlineshop/orders_by_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client__user=self.request.user)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import ProductInstance


class AllOrdersForEmployeeView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all orders, accessible only to employees.
    """
    model = Order
    template_name = 'onlineshop/productinstance_list_all_orders.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.all()


from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import OrderStatusForm, RegisterForm
from .models import Order


def change_status_employee(request, pk):
    """
    View function for changing the status of a specific Order by employee
    """
    order = get_object_or_404(Order, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OrderStatusForm(request.POST, instance=order)

        # Check if the form is valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-orders'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'onlineshop/change_status_employee.html', {'form': form, 'order': order})


class RegisterView(FormView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/sign_up.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        client = Client(user=user)
        client.save()
        return super().form_valid(form)



