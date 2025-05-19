from django.urls import path
from . import views

urlpatterns = [
    path('product-module', views.product_list, name='product-module'),
]

