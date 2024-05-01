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
]