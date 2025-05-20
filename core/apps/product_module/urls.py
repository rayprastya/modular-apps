from django.urls import path
from apps.product_module.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-module'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product-edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]

