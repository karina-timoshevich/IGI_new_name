from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from .models import Employee, Product, ProductType, Order, Client, Manufacturer, UnitOfMeasure, ProductInstance, Cart, \
    PickupLocation, PromoCode, CompanyInfo, Article, FAQ, Job
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import permission_required
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
import calendar
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Employee

log_level_name = os.getenv('LOG_LEVEL', 'INFO')
log_level = getattr(logging, log_level_name.upper(), logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
# Создание обработчика, который записывает логи в файл
handler = logging.FileHandler('app.log')
handler.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from django.utils import timezone


def get_user_time():
    current_time = timezone.localtime(timezone.now())
    user_time_data = {
        "user_timezone": str(timezone.get_current_timezone()),
        "current_date_formatted": current_time.strftime("%d.%m.%Y %H:%M:%S"),
        "calendar_text": current_time.strftime("%B %Y"),
    }
    return user_time_data


def index(request):
    num_products = Product.objects.all().count()
    info = CompanyInfo.objects.first()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    latest_article = Article.objects.latest('date_added')
    current_user_time_data = get_user_time()
    user_timezone = current_user_time_data["user_timezone"]
    current_date_formatted = current_user_time_data["current_date_formatted"]
    calendar_text = current_user_time_data["calendar_text"]

    current_timezone = timezone.get_current_timezone_name()
    now = timezone.now()
    year, month = now.year, now.month
    month_calendar = calendar.monthcalendar(year, month)
    manufacturer_list = Manufacturer.objects.all()
    return render(
        request,
        'index.html',
        context={'num_books': num_products, 'info': info, 'num_authors': num_manufacturers,
                 'num_visits': num_visits,
                 'latest_article': latest_article, 'now': timezone.now(),
                 'current_date_formatted': current_date_formatted, 'calendar_text': calendar_text,
                 'current_timezone': current_timezone, 'month_calendar': month_calendar,
                 'manufacturer_list': manufacturer_list},
    )


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        product_type_id = self.request.GET.get('product_type_id')
        price_order = self.request.GET.get('price_order')
        search_query = self.request.GET.get('search')

        if product_type_id:
            queryset = queryset.filter(product_type_id=product_type_id)

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        if price_order == 'asc':
            queryset = queryset.order_by('price')
        elif price_order == 'desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('name')

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
        dob = form.cleaned_data.get('date_of_birth')
        phone = form.cleaned_data.get('phone_number')
        client = Client(user=user, date_of_birth=dob, phone_number=phone)
        client.save()

        return super().form_valid(form)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = get_object_or_404(Client, user=request.user)
    cart, cart_created = Cart.objects.get_or_create(client=client)
    cart.save()

    product_in_cart = cart.products.filter(product__name=product.name).first()
    if not product_in_cart:
        product_instance = ProductInstance.objects.create(product=product, customer=client, quantity=1)
        cart.products.add(product_instance)
    cart.save()
    logger.info(f'Product {product_id} added to cart')
    cart.update_total_price()
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
        cart.promo_code = promo
        cart.update_total_price()
        cart.save()
        logger.info(f'Promo code {promo_code} applied')
        messages.success(request, 'Promo code applied successfully!')
    except PromoCode.DoesNotExist:
        logger.warning(f'Invalid promo code {promo_code}')
        logger.exception('Invalid promo code')
        messages.error(request, 'Invalid promo code.')
    return redirect('cart')


# @login_required
# def create_order(request):
#     client = get_object_or_404(Client, user=request.user)
#     cart = Cart.objects.get(client=client)
#     total_price = cart.total_price
#     promo_code = cart.promo_code
#     default_discount = PromoCode.objects.first()
#
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.client = client
#             order.total_price = total_price
#             if promo_code:
#                 order.promo_code = promo_code
#             else:
#                 order.discount = default_discount
#             order.save()
#             logger.info(f'Order {order.id} created')
#             for product_instance in cart.products.all():
#                 new_product_instance = ProductInstance.objects.create(
#                     product=product_instance.product,
#                     quantity=product_instance.quantity,
#                     customer=client
#                 )
#                 order.products.add(new_product_instance)
#             cart.products.clear()
#             cart.update_total_price()
#             cart.promo_code = None
#             cart.save()
#             return redirect('my-orders')
#         else:
#             messages.error(request, 'Please select a pickup location.')
#     else:
#         form = OrderForm()
#
#     return render(request, 'onlineshop/user_cart.html', {'form': form, 'cart': cart})
from django.urls import reverse
from yookassa import Configuration, Payment
import uuid


@login_required
def create_order(request):
    client = get_object_or_404(Client, user=request.user)
    cart = Cart.objects.get(client=client)
    total_price = cart.total_price
    promo_code = cart.promo_code
    default_discount = PromoCode.objects.first()

    Configuration.account_id = '464127'
    Configuration.secret_key = 'test_A5adiPpK94uk8ZQXzJJkJ_z3D8X4xslgleMod3njZF4'

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            temp_order = form.save(commit=False)
            temp_order.client = client
            temp_order.total_price = total_price
            if promo_code:
                temp_order.promo_code = promo_code
            else:
                temp_order.discount = default_discount

            return_url = request.build_absolute_uri(reverse('my-orders'))

            payment = Payment.create({
                "amount": {
                    "value": str(total_price),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url
                },
                "capture": True,
                "description": f"Order #{temp_order.id}"
            }, uuid.uuid4())

            if payment.status == 'waiting_for_capture':
                temp_order.save()
                logger.info(f'Order {temp_order.id} created')
                for product_instance in cart.products.all():
                    new_product_instance = ProductInstance.objects.create(
                        product=product_instance.product,
                        quantity=product_instance.quantity,
                        customer=client
                    )
                    temp_order.products.add(new_product_instance)
                cart.products.clear()
                cart.update_total_price()
                cart.promo_code = None
                cart.save()

            return redirect(payment.confirmation.confirmation_url)
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
    template_name = 'onlineshop/reviews.html'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'onlineshop/add_review.html'
    success_url = '/onlineshop/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LogoutView(TemplateView):
    template = 'registration/logout.html'


from django.shortcuts import render
from .models import CompanyInfo


def privacy_policy(request):
    info = CompanyInfo.objects.first()
    return render(request, 'onlineshop/privacy_policy.html', {'info': info})


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


def employee_table(request):
    # Получаем все данные сотрудников
    employees = Employee.objects.all()

    # Фильтрация
    filter_value = request.GET.get('filter', '').strip().lower()
    filter_column = request.GET.get('column', '')

    if filter_value and filter_column in ['first_name', 'last_name', 'position', 'phone', 'email']:
        filter_kwargs = {f"{filter_column}__icontains": filter_value}
        employees = employees.filter(**filter_kwargs)

    # Пагинация
    paginator = Paginator(employees, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'onlineshop/employee_table.html', {
        'page_obj': page_obj,
        'filter': filter_value,
        'column': filter_column,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
import re
from .models import Employee


def add_employee(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        photo = request.FILES.get('photo')
        job_description = request.POST.get('job_description')
        phone = request.POST.get('phone')
        username = request.POST.get('username')  # Используем username для логина
        email = request.POST.get('email')  # Email сотрудника
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        url = request.POST.get('url')

        # Проверка пароля
        if password != password_confirmation:
            return render(request, 'onlineshop/add_employee.html', {
                'error_message': 'Passwords do not match',
                'form_data': request.POST,
            })

        # Проверка телефона
        if not validate_phone(phone):
            return render(request, 'onlineshop/add_employee.html', {
                'error_message': 'Invalid phone number',
                'form_data': request.POST,
            })

        # Проверка URL
        if url and not validate_url(url):
            return render(request, 'onlineshop/add_employee.html', {
                'error_message': 'Invalid URL',
                'form_data': request.POST,
            })

        # Создаем пользователя с подтверждением пароля
        user = User.objects.create_user(username=username, password=password, email=email)

        # Добавляем пользователя в группу Employees
        group = Group.objects.get(name='Employees')
        user.groups.add(group)

        # Создаем сотрудника в таблице Employee
        employee = Employee.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            position=position,
            photo=photo,
            job_description=job_description,
            phone=phone,
            email=email,  # Эмейл добавляется в таблицу сотрудника
        )

        return redirect('employee_table')  # Перенаправление на страницу списка сотрудников

    return render(request, 'onlineshop/add_employee.html')


def validate_phone(phone):
    # Исправленный шаблон для проверки номеров телефона
    phone_pattern = r'^(?:\+375|8)\s?\(?\d{2,3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
    return re.match(phone_pattern, phone)


def validate_url(url):
    # Проверка URL с использованием регулярных выражений
    url_pattern = r'^(https?:\/\/)[\w-]+\.[a-z]{2,6}(\.[a-z]{2})?(\/[\w\-\.]*)*(\.php|\.html)$'
    return re.match(url_pattern, url)


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product  # Импортируйте модель вашего товара


def product_list(request):
    # Получаем все товары
    product_list = Product.objects.all()

    # Создаем пагинатор, показываем 3 товара на странице
    paginator = Paginator(product_list, 3)  # Показываем по 3 товара на странице
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметров
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы

    # Передаем данные в шаблон
    return render(request, 'product_list.html', {'page_obj': page_obj})

import math
from django.shortcuts import render

# Функция для расчета ряда Тейлора для e^x
def taylor_series_expansion(x, n_terms=10):
    result = 0
    for n in range(n_terms):
        result += (x ** n) / math.factorial(n)
    return result

# Генерация данных
def generate_exp_graph_data():
    # Более узкий диапазон для x, который лучше демонстрирует поведение экспоненты
    x_values = [i * 0.1 for i in range(-50, 71)]  # Значения x от -2 до 2 с шагом 0.1
    exp_values = [math.exp(x) for x in x_values]  # Реальные значения e^x
    taylor_values = [taylor_series_expansion(x) for x in x_values]  # Приближение по ряду Тейлора

    return {
        'x_values': x_values,
        'exp_values': exp_values,
        'taylor_values': taylor_values,
    }


@login_required
def employee_stats(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    clients = Client.objects.all()

    total_sales = orders.aggregate(Sum('total_price'))['total_price__sum']
    avg_sales = orders.aggregate(Avg('total_price'))['total_price__avg']
    sales_values = [order.total_price for order in orders]
    median_sales = np.median(sales_values)
    mode_sales = max(set(sales_values), key=sales_values.count)

    client_ages = [(date.today() - client.date_of_birth).days // 365 for client in clients if client.date_of_birth]
    avg_client_age = np.mean(client_ages)
    median_age = np.median(client_ages)

    popular_product_type = products.values('product_type__name').annotate(count=Count('product_type')).order_by(
        '-count').first()
    profitable_product_type = products.values('product_type__name').annotate(profit=Sum('price')).order_by(
        '-profit').first()
    logger.info(
        f'Calculated employee stats: total_sales={total_sales}, avg_sales={avg_sales}, median_sales={median_sales}, mode_sales={mode_sales}, avg_client_age={avg_client_age}, median_age={median_age}, popular_product_type={popular_product_type}, profitable_product_type={profitable_product_type}')

    product_types = Product.objects.values('product_type__name').annotate(
        count=Count('productinstance__order')).order_by(
        '-count')  # группируем продукты по типу и считаем количество заказов
    fig, ax = plt.subplots()  # создаем фигуру для графика
    ax.pie([pt['count'] for pt in product_types], labels=[pt['product_type__name'] for pt in product_types],
           autopct='%1.1f%%')  # для круговой диаграммы, точность 1 знак посл ,
    ax.axis('equal')  # делаем кругляшком

    buf = BytesIO()  # создаем буфер чтобы не в файл кидать
    plt.savefig(buf, format='png')
    plt.close(fig)
    image_string = base64.b64encode(buf.getvalue()).decode()  # переводим в строку прежде кодируя в base64
    data = generate_exp_graph_data()
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
        'x_values': data['x_values'],
        'exp_values': data['exp_values'],
        'taylor_values': data['taylor_values'],
    }

    return render(request, 'onlineshop/employee_stats.html', context)


# Представление для отображения графика


