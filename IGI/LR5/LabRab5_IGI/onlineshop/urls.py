from django.urls import path
from . import views
from django.urls import re_path

from .views import AllClientsForEmployeeView

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('products/', views.ProductListView.as_view(), name='products'),
#
#
#     path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
# ]

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^products/$', views.ProductListView.as_view(), name='products'),
    re_path(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^manufacturers/$', views.ManufacturerListView.as_view(), name='manufacturers'),
    re_path(r'^manufacturers/(?P<pk>\d+)$', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
]
urlpatterns += [
    re_path(r'^myproducts/$', views.OrderedProductsByUserListView.as_view(), name='my-ordered'),
]
urlpatterns += [
    re_path(r'^all-orders/$', views.AllOrdersForEmployeeView.as_view(), name='all-orders'),
]
urlpatterns += [
    re_path(r'^order/(?P<pk>[-\w]+)/change-status/$', views.change_status_employee, name='change-status-employee'),

]
urlpatterns += [
    re_path(r'^orders/$', views.OrdersByUserListView.as_view(), name='my-orders'),
]
urlpatterns += [
    re_path(r'^orders/(?P<order_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.OrderedProductsByUserListView.as_view(), name='order-detail'),
]
urlpatterns += [
    # ... your other url patterns here ...

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
urlpatterns += [
    re_path(r'^cart/$', views.CartView.as_view(), name='cart'),
]
urlpatterns += [
    path('create-order/', views.create_order, name='create-order'),
]

urlpatterns += [
    re_path(r'^increase-quantity/(?P<product_instance_id>[0-9a-f-]+)/$', views.increase_quantity,
            name='increase-quantity'),
    re_path(r'^decrease-quantity/(?P<product_instance_id>[0-9a-f-]+)/$', views.decrease_quantity,
            name='decrease-quantity'),
    re_path(r'^remove-from-cart/(?P<product_instance_id>[0-9a-f-]+)/$', views.remove_from_cart,
            name='remove-from-cart'),
]

urlpatterns += [
    path('onlineshop/cart/apply-promo-code/', views.apply_promo_code, name='apply-promo-code'),
]
urlpatterns += [
    path('promo-codes/', views.PromoCodeListView.as_view(), name='promo-codes'),
]
urlpatterns += [
    path('pickup-locations/', views.PickupLocationListView.as_view(), name='pickup-locations'),
]
urlpatterns += [
    path('clients/', views.client_list, name='clients'),
]

urlpatterns += [
    path('clients/all/', views.AllClientsForEmployeeView.as_view(), name='all-clients'),
]
from .views import EmployeeListView

urlpatterns += [
    path('contacts/', EmployeeListView.as_view(), name='contacts'),
]
from .views import ReviewListView, ReviewCreateView

urlpatterns += [
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('reviews/add/', ReviewCreateView.as_view(), name='add-review'),
]