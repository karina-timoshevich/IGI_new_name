from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .models import Employee, Product, ProductType, Order, Client, Manufacturer, UnitOfMeasure, ProductInstance, Cart, \
    PickupLocation, PromoCode, CompanyInfo, Article, FAQ, Job
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import OrderStatusForm, RegisterForm, OrderForm
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import Cart
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Avg, Count, Sum, Q
from django.shortcuts import render
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from django.views.generic import ListView, CreateView
from .models import Review
from .forms import ReviewForm
import logging
import os

log_level_name = os.getenv('LOG_LEVEL', 'INFO')  # Значение по умолчанию - 'INFO'
log_level = getattr(logging, log_level_name.upper(), logging.INFO)

# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Создание обработчика, который записывает логи в файл
handler = logging.FileHandler('app.log')
handler.setLevel(log_level)

# Создание форматтера
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Добавление форматтера к обработчику
handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(handler)


def get_cat_fact():
    response = requests.get('https://catfact.ninja/fact')
    if response.status_code == 200:
        logger.info('Successfully retrieved cat fact')
        return response.json()
    else:
        logger.warning('Failed to retrieve cat fact')
        return None


def get_random_dog_image():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    if response.status_code == 200:
        return response.json()
    else:
        return None


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

    # Получение данных от API
    cat_fact = get_cat_fact()
    if cat_fact is None:
        logger.warning('Failed to retrieve cat fact')
    dog_image = get_random_dog_image()
    if dog_image is None:
        logger.warning('Failed to retrieve dog image')
    latest_article = Article.objects.latest('date_added')
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_products, 'num_authors': num_manufacturers,
                 'num_visits': num_visits, 'cat_fact': cat_fact, 'dog_image': dog_image,  'latest_article': latest_article},

    )


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        product_type_id = self.request.GET.get('product_type_id')
        price_order = self.request.GET.get('price_order')
        search_query = self.request.GET.get('search')

        if product_type_id:
            queryset = queryset.filter(product_type_id=product_type_id)

        if self.request.user.is_superuser or self.request.user.groups.filter(name='Employees').exists():
            queryset = queryset.order_by('name')
        elif price_order == 'asc':
            queryset = queryset.order_by('price')
        elif price_order == 'desc':
            queryset = queryset.order_by('-price')

        if search_query:
            queryset = queryset.filter(Q(name__istartswith=search_query))
        logger.info(
            f'Filtering products with product_type_id={product_type_id}, price_order={price_order}, search_query={search_query}')
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


class AllOrdersForEmployeeView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all orders, accessible to employees and superusers.
    """
    model = Order
    template_name = 'onlineshop/productinstance_list_all_orders.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.groups.filter(name='Employees').exists():
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.all().order_by('-order_date')


def change_status_employee(request, pk):
    """
    View function for changing the status of a specific Order by employee
    """
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            logger.info(f'Order {pk} status changed')
            return HttpResponseRedirect(reverse('all-orders'))

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
    logger.info(f'Product {product_id} added to cart')
    cart.update_total_price()  # Обновляем общую стоимость в корзине
    return redirect('products')


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


def apply_promo_code(request):
    promo_code = request.POST.get('promo_code')
    try:
        promo = PromoCode.objects.get(code=promo_code)
        cart = Cart.objects.get(client=request.user.client)
        cart.promo_code = promo  # save the promo code in the cart
        cart.update_total_price()
        cart.save()
        logger.info(f'Promo code {promo_code} applied')
        messages.success(request, 'Promo code applied successfully!')
    except PromoCode.DoesNotExist:
        logger.warning(f'Invalid promo code {promo_code}')
        logger.exception('Invalid promo code')
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
            logger.info(f'Order {order.id} created')
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


@login_required
def increase_quantity(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    product_instance.quantity += 1
    product_instance.save()
    logger.info(f'Quantity of product instance {product_instance_id} increased')
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
        logger.info(f'Quantity of product instance {product_instance_id} decreased')
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.update_total_price()
    cart.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, product_instance_id):
    product_instance = get_object_or_404(ProductInstance, id=product_instance_id)
    cart = get_object_or_404(Cart, client=request.user.client)
    cart.products.remove(product_instance)
    product_instance.delete()
    logger.info(f'Product instance {product_instance_id} removed from cart')
    cart.update_total_price()
    cart.save()
    return redirect('cart')


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


class EmployeeListView(generic.ListView):
    model = Employee
    template_name = 'onlineshop/employee_list.html'


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


@login_required
def employee_stats(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    clients = Client.objects.all()

    # Вычисление статистических показателей
    total_sales = orders.aggregate(Sum('total_price'))['total_price__sum']
    avg_sales = orders.aggregate(Avg('total_price'))['total_price__avg']
    sales_values = [order.total_price for order in orders]
    median_sales = np.median(sales_values)
    mode_sales = max(set(sales_values), key=sales_values.count)

    # Вычисление возраста каждого клиента
    client_ages = [(date.today() - client.date_of_birth).days // 365 for client in clients if client.date_of_birth]
    avg_client_age = np.mean(client_ages)
    median_age = np.median(client_ages)

    popular_product_type = products.values('product_type__name').annotate(count=Count('product_type')).order_by(
        '-count').first()
    profitable_product_type = products.values('product_type__name').annotate(profit=Sum('price')).order_by(
        '-profit').first()
    logger.info(
        f'Calculated employee stats: total_sales={total_sales}, avg_sales={avg_sales}, median_sales={median_sales}, mode_sales={mode_sales}, avg_client_age={avg_client_age}, median_age={median_age}, popular_product_type={popular_product_type}, profitable_product_type={profitable_product_type}')

    # Создание круговой диаграммы
    product_types = Product.objects.values('product_type__name').annotate(
        count=Count('productinstance__order')).order_by('-count')
    fig, ax = plt.subplots()
    ax.pie([pt['count'] for pt in product_types], labels=[pt['product_type__name'] for pt in product_types],
           autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Сохранение диаграммы в формате PNG
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)

    # Кодирование изображения в base64 и декодирование в строку
    image_string = base64.b64encode(buf.getvalue()).decode()

    # Передача показателей в шаблон
    context = {
        'total_sales': total_sales,
        'avg_sales': avg_sales,
        'median_sales': median_sales,
        'mode_sales': mode_sales,
        'avg_client_age': avg_client_age,
        'median_age': median_age,
        'popular_product_type': popular_product_type,
        'profitable_product_type': profitable_product_type,
        'pie_chart': image_string,
    }

    return render(request, 'onlineshop/employee_stats.html', context)


class LogoutView(View):
    success_url = reverse_lazy('index')

    def get(self, request):
        logout(request)
        logger.info(f'User logged out')
        return redirect(self.success_url)


def privacy_policy(request):
    return render(request, 'onlineshop/privacy_policy.html')


def news(request):
    articles = Article.objects.all()
    return render(request, 'onlineshop/news.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'onlineshop/article_detail.html', {'article': article})


def about(request):
    info = CompanyInfo.objects.first()
    return render(request, 'onlineshop/about.html', {'info': info})


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'onlineshop/faq.html', {'faqs': faqs})


def jobs(request):
    jobs = Job.objects.all()
    return render(request, 'onlineshop/jobs.html', {'jobs': jobs})