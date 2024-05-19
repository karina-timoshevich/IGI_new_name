from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import FormView

from .models import Employee, Product, ProductType, Order, Client, Manufacturer, UnitOfMeasure, ProductInstance, Cart, \
    PickupLocation

from django.contrib.auth.decorators import login_required


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
        return Order.objects.filter(client__user=self.request.user).order_by('-order_date')


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
        return Order.objects.all().order_by('-order_date')


from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import OrderStatusForm, RegisterForm, OrderForm
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

        # Get the additional fields from the form
        dob = form.cleaned_data.get('date_of_birth')
        phone = form.cleaned_data.get('phone_number')

        # Create a new Client object and save the additional fields
        client = Client(user=user, date_of_birth=dob, phone_number=phone)
        client.save()

        return super().form_valid(form)


from django.shortcuts import redirect, get_object_or_404
from .models import Product, ProductInstance, Client


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = get_object_or_404(Client, user=request.user)
    cart, cart_created = Cart.objects.get_or_create(client=client)
    cart.save()
    # Проверяем, есть ли уже в корзине продукт с таким же именем
    product_in_cart = cart.products.filter(product__name=product.name).first()
    if not product_in_cart:
        # Если такого продукта еще нет, создаем новый экземпляр продукта
        product_instance = ProductInstance.objects.create(product=product, customer=client, quantity=1)
        cart.products.add(product_instance)
    cart.save()
    cart.update_total_price()  # Обновляем общую стоимость в корзине
    return redirect('products')


from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import Cart

from django.contrib.auth.mixins import LoginRequiredMixin


class CartView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'onlineshop/user_cart.html'

    def get_object(self, queryset=None):
        client = get_object_or_404(Client, user=self.request.user)
        cart, created = Cart.objects.get_or_create(client=client)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm()
        return context


from django.shortcuts import redirect
from .models import Order

from django.shortcuts import redirect
from django.contrib import messages
from .models import PromoCode


def apply_promo_code(request):
    promo_code = request.POST.get('promo_code')
    try:
        promo = PromoCode.objects.get(code=promo_code)
        cart = Cart.objects.get(client=request.user.client)
        cart.promo_code = promo  # save the promo code in the cart
        cart.update_total_price()
        cart.save()
        messages.success(request, 'Promo code applied successfully!')
    except PromoCode.DoesNotExist:
        messages.error(request, 'Invalid promo code.')
    return redirect('cart')


@login_required
def create_order(request):
    client = get_object_or_404(Client, user=request.user)
    cart = Cart.objects.get(client=client)  # Get the cart from the database again
    total_price = cart.total_price  # Save the total_price before clearing the cart
    promo_code = cart.promo_code  # Save the promo code before clearing the cart
    default_discount = PromoCode.objects.first()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.total_price = total_price  # Use the saved total_price
            if promo_code:
                order.promo_code = promo_code  # Use the entered promo code
            else:
                order.discount = default_discount  # Use the default discount if no promo code was entered
            order.save()
            for product_instance in cart.products.all():
                # Create a new product instance for each product in the cart
                new_product_instance = ProductInstance.objects.create(
                    product=product_instance.product,
                    quantity=product_instance.quantity,
                    customer=client
                )
                order.products.add(new_product_instance)
            cart.products.clear()
            cart.update_total_price()  # Update the total_price in the cart after clearing the products
            cart.promo_code = None  # Clear the promo code in the cart
            cart.save()
            return redirect('my-orders')
        else:
            messages.error(request, 'Please select a pickup location.')
    else:
        form = OrderForm()

    return render(request, 'onlineshop/user_cart.html', {'form': form, 'cart': cart})

    return render(request, 'onlineshop/user_cart.html', {'form': form, 'cart': cart})


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
    product_instance.delete()  # Удаляем ProductInstance
    cart.update_total_price()
    cart.save()
    return redirect('cart')


from django.views import generic
from .models import PromoCode


class PromoCodeListView(generic.ListView):
    model = PromoCode
    template_name = 'onlineshop/promo_code_list.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset()[1:]


class PickupLocationListView(generic.ListView):
    model = PickupLocation
    template_name = 'onlineshop/pickup_location_list.html'


class AllClientsForEmployeeView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all clients, accessible only to employees.
    """
    model = User
    template_name = 'onlineshop/client_list_for_employee.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(groups__name='Shop Members').exclude(username='user').order_by('username')


def client_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        clients = Client.objects.filter(
            Q(user__username__icontains=search_query) | Q(user__email__icontains=search_query))
    else:
        clients = Client.objects.all().order_by('user__username')

    return render(request, 'onlineshop/client_list_for_employee.html', {'object_list': clients})


from django.views import generic
from .models import Employee

class EmployeeListView(generic.ListView):
    model = Employee
    template_name = 'onlineshop/employee_list.html'


from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review
from .forms import ReviewForm

class ReviewListView(ListView):
    model = Review
    template_name = 'onlineshop/reviews.html'  # update this to your template

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'onlineshop/add_review.html'  # update this to your template
    success_url = '/onlineshop/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)