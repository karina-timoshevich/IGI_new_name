from django.urls import path
from . import views
from django.urls import re_path

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