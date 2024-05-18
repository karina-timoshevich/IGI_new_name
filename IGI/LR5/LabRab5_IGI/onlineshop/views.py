from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView

from .models import Employee, Product, ProductType, Order, Client, Manufacturer, UnitOfMeasure, ProductInstance, Cart


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

# views.py
from django.views import generic
from .models import Product, ProductType


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        product_type_id = self.request.GET.get('product_type_id')
        price_order = self.request.GET.get('price_order')

        if product_type_id:
            queryset = queryset.filter(product_type_id=product_type_id)

        if price_order == 'asc':
            queryset = queryset.order_by('price')
        elif price_order == 'desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.all()
        return context


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


from django.shortcuts import redirect, get_object_or_404
from .models import Product, ProductInstance, Client


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = get_object_or_404(Client, user=request.user)
    product_instance, product_created = ProductInstance.objects.get_or_create(product=product, customer=client)
    cart, cart_created = Cart.objects.get_or_create(client=client)
    cart.save()
    if not product_created:
        product_instance.quantity += 1
        product_instance.save()
    else:
        cart.products.add(product_instance)
        cart.save()
    cart.update_total_price()  # Обновляем общую стоимость в корзине
    return redirect('products')


from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import Cart


class CartView(DetailView):
    model = Cart
    template_name = 'onlineshop/user_cart.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Cart, client=self.request.user.client)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Order

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, client=request.user.client)
    order = Order(client=request.user.client)
    order.save()
    for product_instance in cart.products.all():
        order.products.add(product_instance)
    cart.products.clear()
    cart.save()
    return redirect('my-orders')

@login_required
def increase_quantity(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    product_instance.quantity += 1
    product_instance.save()
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.update_total_price()
    cart.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    if product_instance.quantity > 1:
        product_instance.quantity -= 1
        product_instance.save()
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.update_total_price()
    cart.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.products.remove(product_instance)
    cart.update_total_price()
    cart.save()
    return redirect('cart')